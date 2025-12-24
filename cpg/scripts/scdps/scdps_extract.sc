import io.shiftleft.codepropertygraph.generated.nodes._
import io.shiftleft.semanticcpg.language._
import scala.collection.mutable

// =========================================
// REQUIRED: PROGRAM SCOPING
// =========================================
val targetFile =
  sys.env.getOrElse(
    "TARGET_FILE",
    throw new RuntimeException("TARGET_FILE not set")
  )

// =========================================
// SIMPLE MUTABLE COUNTER (SANDBOX-PROVEN)
// =========================================
final class Counter(var value: Int)

// =========================================
// FROZEN PARAMETERS
// =========================================
val MAX_DEPTH = 3
val MAX_PATHS_PER_START = 1000

// =========================================
// ALLOWED NODE LABELS (FROZEN)
// =========================================
val allowedNodeLabels = Set(
  "IDENTIFIER",
  "CALL",
  "LITERAL",
  "METHOD_PARAMETER_IN",
  "METHOD_PARAMETER_OUT",
  "RETURN",
  "METHOD_RETURN"
)

// =========================================
// VALID START NODES (SANDBOX-ALIGNED)
// =========================================
def isValidStart(n: StoredNode): Boolean =
  n.label match {
    case "METHOD_PARAMETER_IN" => true
    case "IDENTIFIER"          => true
    case "CALL"                => true
    case _                     => false
  }

// =========================================
// LOW-INFORMATION PRUNING
// =========================================
def isLowInformation(prev: String, next: String): Boolean =
  prev == "IDENTIFIER" && next == "IDENTIFIER"

// =========================================
// GLOBAL HISTOGRAM
// =========================================
val scdpsCounts =
  mutable.Map[String, Int]().withDefaultValue(0)

// =========================================
// DFS — PDG-BASED, BOUNDED, DETERMINISTIC
// =========================================
def dfs(
  current: StoredNode,
  depth: Int,
  visited: Set[Long],
  path: List[String],
  lastEdgeWasControl: Boolean,
  pathCounter: Counter
): Unit = {

  if (depth == MAX_DEPTH) return
  if (current.label == "LITERAL") return
  if (pathCounter.value >= MAX_PATHS_PER_START) return

  // ---------- DATA DEPENDENCE ----------
  for (next <- current._reachingDefOut.sortBy(_.id)) {
    if (
      !visited.contains(next.id) &&
      allowedNodeLabels.contains(next.label) &&
      !isLowInformation(current.label, next.label)
    ) {
      val newPath = path ++ List("DATA_DEP", next.label)
      val sig = newPath.mkString("-")

      scdpsCounts(sig) += 1
      pathCounter.value += 1

      dfs(
        next,
        depth + 1,
        visited + next.id,
        newPath,
        lastEdgeWasControl = false,
        pathCounter
      )
    }
  }

  // ---------- CONTROL DEPENDENCE (ONE STEP) ----------
  if (!lastEdgeWasControl) {
    for (next <- current._cdgOut.sortBy(_.id)) {
      if (
        !visited.contains(next.id) &&
        allowedNodeLabels.contains(next.label)
      ) {
        val newPath = path ++ List("CONTROL_DEP", next.label)
        val sig = newPath.mkString("-")

        scdpsCounts(sig) += 1
        pathCounter.value += 1

        dfs(
          next,
          depth + 1,
          visited + next.id,
          newPath,
          lastEdgeWasControl = true,
          pathCounter
        )
      }
    }
  }
}

// =========================================
// MAIN — METHOD SELECTION (PIPELINE-SAFE)
// =========================================
for (
  m <- cpg.method
         .filter(_.filename.endsWith(targetFile))
         .filterNot(_.name == "main")
         .filter(_.ast.isControlStructure.nonEmpty)
         .l
) {

  val rawNodes =
    (m._reachingDefOut.l ++ m._cdgOut.l)
      .distinct
      .sortBy(_.id)

  val startNodes = rawNodes.filter(isValidStart)

  for (n <- startNodes) {
    dfs(
      current = n,
      depth = 0,
      visited = Set(n.id),
      path = List(n.label),
      lastEdgeWasControl = false,
      pathCounter = new Counter(0)
    )
  }
}

// =========================================
// JSON OUTPUT (STDOUT ONLY)
// =========================================
println("{")
println(
  scdpsCounts.toSeq
    .sortBy(_._1)
    .map { case (k, v) => s""""$k": $v""" }
    .mkString(",\n")
)
println("}")

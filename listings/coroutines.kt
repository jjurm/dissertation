/** Evaluate given metrics on the graph */
fun CoroutineScope.evaluateMetricsAsync(
        metrics: Collection<MetricInfo>,
        graph: Graph,
        callback: suspend (graph: Graph, results: List<MetricResult>) -> Unit = { _, _ -> }
): Deferred<Unit> {
    // Returns a list of metrics they need to be computed in, as some reuse values of others
    val metricsToCompute: List<MetricInfo> = metrics.topologicalOrderWithDependencies()

    return async {
        metricsToCompute
                // An instance of each [Metric] is created by invoking the [factory] field
                .map { metric -> metric.factory() }
                .run {
                    // Run evaluation on each graph, clean up auxiliary data
                    val results: List<MetricResult> = map { it.evaluate(graph) }.filterNotNull()
                    forEach { it.cleanup(graph) }
                    // Return results: flags marking the outcome of each metric
                    results
                }
                // Run callback (only if there are any new results)
                .takeIf { it.isNotEmpty() }
                ?.let { callback(graph, it) }
    }
}

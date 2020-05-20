SELECT g.EXPERIMENT as experiment, g.DATASET as dataset, p.ID as graph_id,
       t.METRIC as metric, t.TIME as time
       -- p.HASH as graph_hash, p.GRAPHSTREAMID as graph_name
FROM PERTURBEDGRAPH_TIMINGS t
LEFT JOIN PERTURBEDGRAPH p on t.PERTURBEDGRAPH = p.ID
LEFT JOIN GRAPHCOLLECTION g on p.GRAPHCOLLECTION = g.ID
WHERE g.EXPERIMENT IN ('reproduce', 'random-edges', 'unscored')

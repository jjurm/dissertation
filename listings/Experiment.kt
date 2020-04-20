package uk.ac.cam.jm2186.graffs.db.model

import org.hibernate.annotations.LazyCollection
import org.hibernate.annotations.LazyCollectionOption
import uk.ac.cam.jm2186.graffs.db.NamedEntity
import uk.ac.cam.jm2186.graffs.graph.storage.GraphDatasetId
import uk.ac.cam.jm2186.graffs.metric.MetricId
import uk.ac.cam.jm2186.graffs.robustness.RobustnessMeasureId
import javax.persistence.*

@Entity
class Experiment(
        name: String,

        @ManyToOne(fetch = FetchType.EAGER)
        var generator: GraphGenerator,
        @ElementCollection(fetch = FetchType.EAGER)
        var metrics: Set<MetricId> = mutableSetOf(),
        @ElementCollection(fetch = FetchType.EAGER)
        var robustnessMeasures: Set<RobustnessMeasureId> = mutableSetOf(),

        datasets: Collection<GraphDatasetId> = listOf()
) : NamedEntity(name) {

    @OneToMany(mappedBy = "experiment", cascade = [CascadeType.ALL], orphanRemoval = true)
    @LazyCollection(LazyCollectionOption.FALSE)
    var graphCollections: MutableList<GraphCollection> = datasets.map { GraphCollection(it, this) }.toMutableList()

    @OneToMany(mappedBy = "experiment", cascade = [CascadeType.REMOVE], orphanRemoval = true)
    @LazyCollection(LazyCollectionOption.FALSE)
    val robustnessResults: MutableList<Robustness> = mutableListOf()

    val datasets get() = graphCollections.map { it.dataset }
}
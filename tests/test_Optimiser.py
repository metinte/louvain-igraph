import unittest
import igraph as ig
import louvain

class OptimiserTest(unittest.TestCase):

  def setUp(self):
    self.optimiser = louvain.Optimiser();

  def test_move_nodes(self):
    G = ig.Graph.Full(100);
    partition = louvain.CPMVertexPartition(G, resolution_parameter=0.5);
    self.optimiser.move_nodes(partition, consider_comms=louvain.ALL_NEIGH_COMMS);
    self.assertListEqual(
        partition.sizes(), [100],
        msg="CPMVertexPartition(resolution_parameter=0.5) of complete graph after move nodes incorrect.");

  def test_merge_nodes(self):
    G = ig.Graph.Full(100);
    partition = louvain.CPMVertexPartition(G, resolution_parameter=0.5);
    self.optimiser.merge_nodes(partition, consider_comms=louvain.ALL_NEIGH_COMMS);
    self.assertListEqual(
        partition.sizes(), [100],
        msg="CPMVertexPartition(resolution_parameter=0.5) of complete graph after merge nodes incorrect.");

  def test_diff_move_node_optimality(self):
    G = ig.Graph.Erdos_Renyi(100, p=5./100, directed=False, loops=False);
    partition = louvain.CPMVertexPartition(G, resolution_parameter=0.1);
    while 0 < self.optimiser.move_nodes(partition, consider_comms=louvain.ALL_NEIGH_COMMS):
      pass;
    for v in G.vs:
      neigh_comms = set(partition.membership[u.index] for u in v.neighbors());
      for c in neigh_comms:
        self.assertLessEqual(
          partition.diff_move(v.index, c), 0,
          msg="Was able to move a node to a better community, violating node optimality.");

  def test_optimiser(self):
    G = reduce(ig.Graph.disjoint_union, (ig.Graph.Tree(10, 3, mode=ig.TREE_UNDIRECTED) for i in range(10)));
    partition = louvain.CPMVertexPartition(G, resolution_parameter=0);
    self.optimiser.consider_comms=louvain.ALL_NEIGH_COMMS;
    self.optimiser.optimise_partition(partition);
    self.assertListEqual(
        partition.sizes(), 10*[10],
        msg="After optimising partition failed to find different components with CPMVertexPartition(resolution_parameter=0)");

  def test_neg_weight_bipartite(self):
    G = ig.Graph.Full_Bipartite(50, 50);
    G.es['weight'] = -0.1;
    partition = louvain.CPMVertexPartition(G, resolution_parameter=-0.1, weight='weight');
    self.optimiser.consider_comms=louvain.ALL_COMMS;
    self.optimiser.optimise_partition(partition);
    self.assertListEqual(
        partition.sizes(), 2*[50],
        msg="After optimising partition failed to find bipartite structure with CPMVertexPartition(resolution_parameter=-0.1)");

#%%
if __name__ == '__main__':
  #%%
  unittest.main(verbosity=3);
  suite = unittest.TestLoader().discover('.');
  unittest.TextTestRunner(verbosity=1).run(suite);
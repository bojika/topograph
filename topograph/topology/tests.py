from django.test import TestCase

# Create your tests here.

from django.urls import reverse
from django.contrib.auth import get_user_model
from datetime import datetime
from django.utils import timezone

from topology.models import Edge, Node, Topology


class TopologyModelViewTest(TestCase):
    def setUp(self):
        topology = Topology.objects.create(id=1, description='Test Topology')
        node1 = Node.objects.create(id=1,
                            label="R1",
                            meta_data='{"db_id": 1, "id": "10.0.0.1"}',
                            x=10,
                            y=10,
                            topology=topology)
        node2 = Node.objects.create(id=2,
                            label="R2",
                            meta_data='{"db_id": 2, "id": "10.0.0.2"}',
                            x=20,
                            y=20,
                            topology=topology)
        Edge.objects.create(id=1,
                            begin=node1,
                            end=node2,
                            cost=30,
                            meta_data='{"db_id": 1, "IPv4_ADDRESS": "10.0.1.0/32"}')

    def test_topology_model(self):
        topology = Topology.objects.get(id=1)
        url_for_topology = reverse('topology_detail', kwargs={'pk': topology.pk})
        self.assertTrue(isinstance(topology, Topology))
        self.assertEqual(topology.__str__(), topology.description)
        self.assertEqual(topology.get_absolute_url(), url_for_topology)

    def test_node_model(self):
        node = Node.objects.get(id=1)
        self.assertTrue(isinstance(node, Node))
        self.assertTrue(isinstance(node.topology, Topology))
        self.assertEqual(node.__str__(), node.label)

    def test_edge_model(self):
        edge = Edge.objects.get(id=1)
        self.assertTrue(isinstance(edge, Edge))
        self.assertTrue(isinstance(edge.begin.topology, Topology))
        self.assertEqual(edge.__str__(), f'{edge.begin} <--> {edge.end}')

    def test_home(self):
        # print('test_home is running...')
        # Issue a GET request.
        response = self.client.get('/')
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        print(response)

    def test_topology_list_view(self):
        # print('test_topology_list_view is running...')
        response = self.client.get('/topology/list/')
        # for i in response.context:
        #     print("\n")
        #     print(i)
        topo = Topology.objects.all()
        # for i in topo:
        #     print(i.pk, i.description, i.time_created, i.time_updated, i.status)
        # for i in topo:
        #     print(i.pk)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'topology/topology_list.html')
        self.assertEqual(len(response.context['topology_list']), topo.count())
        self.assertEqual(response.context['topology_list'][0], topo.get(id=1))

    def tearDown(self):
        Topology.objects.get(id=1).delete()



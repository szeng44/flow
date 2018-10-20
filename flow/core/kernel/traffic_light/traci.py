from flow.core.kernel.traffic_light import KernelTrafficLight
import traci.constants as tc


class TraCITrafficLight(KernelTrafficLight):
    """

    """

    def __init__(self, master_kernel, kernel_api):
        """

        """
        KernelTrafficLight.__init__(self, master_kernel, kernel_api)

        self.__tls = dict()  # contains current time step traffic light data
        self.__tls_properties = dict()  # traffic light xml properties

        # names of nodes with traffic lights
        self.__ids = kernel_api.trafficlight.getIDList()

        # number of traffic light nodes
        self.num_traffic_lights = len(self.__ids)

        # subscribe the traffic light signal data
        for node_id in self.__ids:
            self.kernel_api.trafficlight.subscribe(
                node_id, [tc.TL_RED_YELLOW_GREEN_STATE])

    def update(self):
        """See parent class."""
        tls_obs = self.kernel_api.trafficlight.getSubscriptionResults()
        self.__tls = tls_obs.copy()

    def get_ids(self):
        """See parent class."""
        return self.__ids

    def set_state(self, node_id, state, link_index="all"):
        """See parent class."""
        if link_index == "all":
            # if lights on all lanes are changed
            self.kernel_api.trafficlight.setRedYellowGreenState(
                tlsID=node_id, state=state)
        else:
            # if lights on a single lane is changed
            self.kernel_api.trafficlight.setLinkState(
                tlsID=node_id, tlsLinkIndex=link_index, state=state)

    def get_state(self, node_id):
        """See parent class."""
        return self.__tls[node_id][tc.TL_RED_YELLOW_GREEN_STATE]

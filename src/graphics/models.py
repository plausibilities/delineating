import os

import pymc as pm
import graphviz


class Models:

    def __init__(self, path: str):
        """

        :param path:
        """

        self.__path = path

    def __draw(self, model: pm.Model, size: str, name: str) -> bool:
        """

        :param model:
        :param size:
        :param name:
        :return:
        """

        # The DAG
        diagram = pm.model_graph.ModelGraph(model=model).make_graph()
        diagram.node_attr.update(shape='circle')
        diagram.graph_attr.update(size=size)

        # Save
        try:
            diagram.save(os.path.join(self.__path, name))
            return True
        except OSError as err:
            raise Exception(err.strerror)

    def exc(self, model: pm.Model, size: str = '5.7,5.9', name: str = 'model.gv') -> None:
        """

        :param model:
        :param size: 'width,height'
        :param name:
        :return:
        """

        drawn = self.__draw(model=model, size=size, name=name)

        if drawn:
            graphviz.render(engine='dot', format='pdf', filepath=os.path.join(self.__path, name))

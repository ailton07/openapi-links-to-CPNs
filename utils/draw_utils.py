
class DrawUtils:

    @staticmethod
    def draw(draws_map, file_name, petri_net):
        """ create a draw called file_name and add the file name and the draw to a map

        Args:
            draws_map (map): a map composed of (file_name, draw)
            file_name (_type_): the file name to the draw
            petri_net (_type_): the petri net which is going to be drawed
        """
        path = 'draws/'
        draws_map[file_name] = petri_net.draw(path + file_name)

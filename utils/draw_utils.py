import os

class DrawUtils:

    DRAWS_DIR = "draws/"

    @staticmethod
    def draw(draws_map, file_name, petri_net):
        """ create a draw called file_name and add the file name and the draw to a map

        Args:
            draws_map (map): a map composed of (file_name, draw)
            file_name (_type_): the file name to the draw
            petri_net (_type_): the petri net which is going to be drawed
        """
        draws_map[file_name] = petri_net.draw(DrawUtils.DRAWS_DIR + file_name)

    @staticmethod
    def clean_draw_dir():
        print(f'Cleaning draw_dir: {DrawUtils.DRAWS_DIR}')
        for filename in os.listdir(DrawUtils.DRAWS_DIR):
            file_path = os.path.join(DrawUtils.DRAWS_DIR, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print('Failed to clean %s: failed to delete %s. Reason: %s' % (DrawUtils.DRAWS_DIR, file_path, e))

import threader

class EchoNest(threader.ComputationThread):
    """
        This thread tries to get data from the echnonest
    """

    def _calculate(self):
        self.data = ''

if __name__ == '__main__':
    threader.main(EchoNest)

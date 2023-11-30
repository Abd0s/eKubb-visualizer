import multiprocessing as mp


class DataProcessingProcess(mp.Process):

    def __init__(self, data_in: mp.Queue, data_out: mp.Queue):
        super().__init__()

    def run(self) -> None:
        """Runs when the process starts"""
        pass

    def process_data(self) -> None:
        pass

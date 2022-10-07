



class TunerConfig:
    def __init__(self):

        self.verbose = 2

        self.cv = 2

        self.n_jobs = -1

    def get_tuner_config(self):
        return self.__dict__
from dataclasses import dataclass
from datetime import time


@dataclass
class Connessione:
    _id : int
    _id_rifugio1 :int
    _id_rifugio2 : int
    _distanza : float
    _difficolta : int
    #durata : time
    _anno : int

    @property
    def id(self) -> int:
        return self._id
    @id.setter
    def id(self, value):
        self._id = value

    @property
    def id_rifugio1(self) -> int:
        return self._id_rifugio1
    @id_rifugio1.setter
    def id_rifugio1(self, value):
        self._id_rifugio1 = value

    @property
    def id_rifugio2(self) -> int:
        return self._id_rifugio2
    @id_rifugio2.setter
    def id_rifugio2(self, value):
        self._id_rifugio2 = value

    @property
    def distanza(self) -> int:
        return self._distanza
    @distanza.setter
    def distanza(self, value):
        self._distanza = value

    @property
    def difficolta(self) -> int:
        return self._difficolta
    @difficolta.setter
    def difficolta(self, value):
        self._difficolta = value

    @property
    def anno(self) -> int:
        return self._anno
    @anno.setter
    def anno(self, value):
        self._anno = value


    def __hash__(self):
        return hash(self.id)
    def __eq__(self, other):
        return self.id == other.id
    def __repr__(self):
        return f"Connessione({self.id}), From {self.id_rifugio1} To {self.id_rifugio2}"



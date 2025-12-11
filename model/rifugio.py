from dataclasses import dataclass

@dataclass
class Rifugio:
    _id_rifugio : int
    _nome :str
    _localita :str
    _altitudine :float
    #capienza :int
    #aperto : int

    @property
    def id_rifugio(self):
        return self._id_rifugio
    @id_rifugio.setter
    def id(self, value):
        self._id_rifugio = value

    @property
    def nome(self):
        return self._nome
    @nome.setter
    def nome(self, value):
        self._nome = value

    @property
    def localita(self):
        return self._localita
    @localita.setter
    def localita(self, value):
        self._localita = value

    @property
    def altitudine(self):
        return self._altitudine
    @altitudine.setter
    def altitudine(self, value):
        self._altitudine = value


    def __hash__(self):
        return hash(self.id_rifugio)
    def __eq__(self, other):
        if other is None:
            return False
        return self.id_rifugio == other.id_rifugio
    def __str__(self):
        return f'[{self.id_rifugio}] {self.nome} ({self.localita})'

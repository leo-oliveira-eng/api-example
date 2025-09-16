from dataclasses import dataclass

@dataclass(frozen=True)
class ISBN:
    text: str

    def __post_init__(self):
        v = self._normalized(self.text)
        if len(v) not in (10, 13) or not v.isdigit():
            raise ValueError("ISBN inválido (esperado 10 ou 13 dígitos).")

    @staticmethod
    def _normalized(s: str) -> str:
        return "".join(ch for ch in s if ch.isdigit())

    def normalized(self) -> str:
        return self._normalized(self.text)

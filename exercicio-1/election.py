
class Election:
    """
    Classe para calcular percentuais de votos em uma eleição.
    """
    def __init__(self, total_voters, valid_votes, blank_votes, null_votes):
        if valid_votes + blank_votes + null_votes > total_voters:
            raise ValueError("A soma dos votos não pode exceder o total de eleitores.")
        self.total_voters = total_voters
        self.valid_votes = valid_votes
        self.blank_votes = blank_votes
        self.null_votes = null_votes

    def valid_votes_percentage(self):
        """Retorna o percentual de votos válidos."""
        return (self.valid_votes / self.total_voters) * 100

    def blank_votes_percentage(self):
        """Retorna o percentual de votos brancos."""
        return (self.blank_votes / self.total_voters) * 100

    def null_votes_percentage(self):
        """Retorna o percentual de votos nulos."""
        return (self.null_votes / self.total_voters) * 100
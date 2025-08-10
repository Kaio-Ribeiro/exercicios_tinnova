
from election import Election

def main():
    election = Election(1000, 600, 300, 100)
    print(f"Percentual de votos válidos: {election.valid_votes_percentage():.2f}%")
    print(f"Percentual de votos brancos: {election.blank_votes_percentage():.2f}%")
    print(f"Percentual de votos nulos: {election.null_votes_percentage():.2f}%")


if __name__ == "__main__":
    main()
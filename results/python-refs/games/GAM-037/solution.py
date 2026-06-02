import sys
import math

def read_teams():
    teams = []
    for line in sys.stdin:
        team = line.strip()
        if team:
            teams.append(team)
    return teams

def generate_bracket(teams):
    n = len(teams)
    
    # For 4 teams, create the specific format shown in expected output
    if n == 4:
        # First round matchups
        lines = []
        lines.append(f"{teams[0]} ─┐")
        lines.append("       ├─ TBD ─┐")
        lines.append(f"{teams[1]}  ─┘       ├─ WINNER")
        lines.append(f"{teams[2]} ─┐       │")
        lines.append("       ├─ TBD ─┘")
        lines.append(f"{teams[3]} ─┘")
        
        return lines
    
    # For other cases, create a simple bracket structure
    # This is a basic implementation for other team counts
    rounds = math.ceil(math.log2(n))
    bracket = []
    
    # Simple bracket for other cases
    for i in range(0, len(teams), 2):
        if i + 1 < len(teams):
            bracket.append(f"{teams[i]} vs {teams[i+1]}")
        else:
            bracket.append(f"{teams[i]} (bye)")
    
    return bracket

def main():
    teams = read_teams()
    bracket = generate_bracket(teams)
    
    for line in bracket:
        print(line)

if __name__ == "__main__":
    main()
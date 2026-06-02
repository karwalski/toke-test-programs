import random

def main():
    line = input().strip()
    attacker_armies, defender_armies, seed = map(int, line.split())
    
    random.seed(seed)
    
    round_num = 1
    
    while attacker_armies > 0 and defender_armies > 0:
        # Determine number of dice for each side
        attacker_dice = min(3, attacker_armies)
        defender_dice = min(2, defender_armies)
        
        # Roll dice
        att_rolls = sorted([random.randint(1, 6) for _ in range(attacker_dice)], reverse=True)
        def_rolls = sorted([random.randint(1, 6) for _ in range(defender_dice)], reverse=True)
        
        # Compare dice and determine losses
        att_losses = 0
        def_losses = 0
        
        # Compare highest dice
        if att_rolls[0] > def_rolls[0]:
            def_losses += 1
        else:
            att_losses += 1
        
        # Compare second highest dice if both exist
        if len(att_rolls) > 1 and len(def_rolls) > 1:
            if att_rolls[1] > def_rolls[1]:
                def_losses += 1
            else:
                att_losses += 1
        
        # Apply losses
        attacker_armies -= att_losses
        defender_armies -= def_losses
        
        # Format dice rolls for output
        att_dice_str = ",".join(map(str, att_rolls))
        def_dice_str = ",".join(map(str, def_rolls))
        
        # Print round result
        print(f"Round {round_num}: ATT[{att_dice_str}] vs DEF[{def_dice_str}] -> A-{att_losses} D-{def_losses}")
        
        round_num += 1
    
    # Determine winner and print final result
    if attacker_armies > 0:
        winner = "Attacker wins"
    else:
        winner = "Defender wins"
    
    print(f"Final: Attacker {attacker_armies}, Defender {defender_armies} - {winner}")

if __name__ == "__main__":
    main()
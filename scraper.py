import requests
from bs4 import BeautifulSoup
import pandas as pd

teams = ['ATL','BRK','BOS','CHO','CHI','CLE','DAL','DEN','DET','GSW','HOU','IND','LAC','LAL','MEM','MIA','MIL','MIN','NOP','NYK','OKC','ORL','PHI','PHO','POR','SAC','SAS','TOR','UTA','WAS']
hist = {
  'games':[]
}
error = []
for curr in teams:
  try:
    URL = f"https://www.basketball-reference.com/teams/{curr}/2022_games.html"
    print(URL)
    r = requests.get(URL)
      
    soup = BeautifulSoup(r.content, 'html.parser')

    table = soup.find('table',attrs = {'id':'games'})

    a = table.findAll('td')
    data = {
      "curr":curr,
    }


    for x in a:
        #game_result

        """
        date_game
        game_start_time
        network
        box_score_text
        game_location
        opp_name
        game_result
        overtimes
        pts
        opp_pts
        wins
        losses
        game_streak
        game_remarks"""
        
        
        if ( x.get('data-stat') == 'opp_name'):
          data['opp_name'] = x.next.next
          
        if ( x.get('data-stat') == 'game_result'):
          data['game_result'] = x.next
        if (x.get('data-stat') == 'pts' ):
          data['pts'] = x.next
        if (x.get('data-stat') == 'opp_pts' ):
          data['opp_pts'] = x.next
        if (x.get('data-stat') == 'wins' ):
          data['wins'] = x.next
        if (x.get('data-stat') == 'losses' ):
          data['losses'] = x.next
        if (x.get('data-stat') == 'game_streak' ):
          data['game_streak'] = x.next
          hist['games'].append(data)
          data = {"curr":curr}
  except:
    error.append(curr)    
print(len(hist) )
df = pd.DataFrame(hist['games'])
df.to_csv("nba_preseason_games_2022.csv", sep=',', encoding='utf-8')


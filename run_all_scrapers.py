from predictions import Predictions
from predictions_valuebets import ValueBets
from volume import Volume

predictions_vanilla = Predictions()
value_bets = ValueBets()
volume_of_bets = Volume()

predictions_vanilla.scrape()
value_bets.scrape()
volume_of_bets.scrape()


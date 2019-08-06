A web intreface to get the top Nth stream from Twitch and return a popout window.

Example Call: http://phx-dash01.hq.phxlabs.net:8100/?idx=0&game=Dauntless&refresh=900

Takes the following Queries:
* idx : The position of the streamer in the list - 0 = Top Streamer, 1 = 2nd, etc - Default:0
* game : The name of the game, accept's spaces - Default "Dauntless"
* refresh : Number of seconds before the page refreshes, as some streamers stop playing or switch games, we need to refresh the page. - Default: 900


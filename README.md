<h1>Chess Database</h1>
<ul>
  <li>Marko Vuckovic</li>
  <li>David Bojanić</li>
  <li>Alem Čaušević</li>
  <li>Royman Jernej</li>
  <li>Stefanija Atanasova</li>
</ul>

<h2>Data</h2>
<p>For this project we choose to use data from multiple sources. These are the data sets we used till now.</p>
<ul>
  <li>https://www.pgnmentor.com/files.html#players</li>
  <li>https://www.kaggle.com/datasets/zq1200/magnus-carlsen-complete-chess-games-20012022</li>
  <li>https://www.kaggle.com/datasets/nelgiriyewithana/countries-of-the-world-2023</li>
</ul> 
<p>First link consists of games played by most famouse players in history of chess. For now we only used data set with games of Magnus Carlsen.
Data in this link is stored in standard way chess games are stored - in .pgn format. Each games consists of information about both players, opening played,
tournament they played in, result, opening played and their ELO (rating).</p>
<p>Second and third links are a standard CSV format of data. In 2nd we have games of magnus carlsen just stored in different way than in 1st one.
Third data set consists of data about every country (population, GDP,...)</p>
<h2>Data Initialization</h2>
<p>We will now explain how we made the data readable and ready to use. For .pgn format we used python library
chess.pgn which allowed us to easily read chess games and their info. </p>
 <pre><code>
  import chess.pgn
  def parse_pgn(file_path):
    games = []
    with open(file_path) as pgn_file:
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break
            games.append(game)
    return games
 </code></pre>
 <p>This function is able to read a standard .pgn file and save context of each game in a list.</p>
 <p>For reading CSV files we used two different methods. Using CSV library in python and pandas.</p>
 <pre><code>
   with open('data/eco_codes.csv', newline='') as csvFile:
    reader = csv.reader(csvFile)
    next(reader)  # We skip the first row
    for row in reader:
        ECO_names[row[0]] = row[1]
 </code></pre>
 <pre><code>
   economic_data = pd.read_csv('economics.csv')
 </code></pre>
 <h2>Type of data</h2>
 <p>Here, we will present some part of our data we used, so you can have a grater picture of how we did our reasrch.</p>
 <pre>[Event "Troll Masters"]
[Site "Gausdal NOR"]
[Date "2001.01.05"]
[Round "1"]
[White "Edvardsen,R"]
[Black "Carlsen,Magnus"]
[Result "1/2-1/2"]
[WhiteElo "2055"]
[BlackElo ""]
[ECO "D12"]
<br>
1.d4 Nf6 2.Nf3 d5 3.e3 Bf5 4.c4 c6 5.Nc3 e6 6.Bd3 Bxd3 7.Qxd3 Nbd7 8.b3 Bd6
9.O-O O-O 10.Bb2 Qe7 11.Rad1 Rad8 12.Rfe1 dxc4 13.bxc4 e5 14.dxe5 Nxe5 15.Nxe5 Bxe5
16.Qe2 Rxd1 17.Rxd1 Rd8 18.Rxd8+ Qxd8 19.Qd1 Qxd1+ 20.Nxd1 Bxb2 21.Nxb2 b5
22.f3 Kf8 23.Kf2 Ke7  1/2-1/2
</pre>
<p>CSV data sets contain same information, just in a little bit different format.</p>
<h2>Questions</h2>
<p>Till now, we were able to answer few of intreeting questions. First thing we did was look what are the most popular openings in chess, 
since the winner can be decided in first 10-15 moves in most cases. Since in this part of game your memory comes to play and 
not your skill, we thought it would be great to know which openings show best results and boost our chanses of winning.
And so, what is better then to look at what best player in the world, Magnus Carlsen, plays.</p>
<p><img src="https://github.com/PastMatter/PR24MVDBACSAJR/assets/73186445/89282555-c41d-4953-b08e-8bcfa4052995" alt=""></p>
<p>And as we can see on the graph most popular openning is Queen's pawn gamit and Sicilian defense. Ofcourse, these are the opening played 
by Magnus Carlsen and I am sure none of us can play like him, but this is just a great starting point for everyone who wants to play
chess seriously.</p>
<p>Next question we answered was if players performance decreses over time like in other sports. In other sports people, for example footbal,
players usually retire when they reach 35 years. There are also some other factors, like injuries, but we do not have that in chess :).
And then again, we choose to look into Carlsen's progress over years.</p>
<p><img src="https://github.com/PastMatter/PR24MVDBACSAJR/assets/73186445/5e3ed408-5dc4-4c04-8982-d3fb6ca04f27" alt=""></p>
<p>As shown in the graph, Magnus has been consistent for almost 20 years of his career with around 75% win-rate from 2005 all over to 2022.</p>
<p>Now let's hop into the world of economics. And our question is is GDP of a country in any correlation with number of high rated players in that same country.
This is where the data set with country information came in hadny. We looked into countries with highest GDP and number of high rated players from that countries and found out
that there is no correlation between those two.</p>
<p><img src="https://github.com/PastMatter/PR24MVDBACSAJR/assets/73186445/a3a15a0d-bb92-4119-b762-eb2cb4b665f3" alt=""></p>
<p>And for the final question, we tried to show the distribution of ratings which might seem interesting to someone, since you can compare your own rating (if you play chess)
with rating of other players and see in which group you belong to.</p>
<p><img src="https://github.com/PastMatter/PR24MVDBACSAJR/assets/73186445/2a89eb67-6e1c-4e5f-9b6b-99cbe8d8fd36" alt=""></p>
<h2>Future Plans</h2>
<p>Since this topic opens a lot of questions, especially to people interested in chess we cannot answer all of them. But we will try to answer some of the most interesting ones.
One of them is what are the best tournaments in the world. We will do that by looking at the people that played on that tournaments and find the average rating of each tournament.
Additionaly, we might try do something with women chess and compare it to men. And ofcourse, for the final project we will try to make a pleayable chess board. The idea is that each time 
a move is pleyed we can get some information about the current position (what are the most plaeyd moves, win-ration of white and black in that position, which players played that same postion
and is that postion usually played by high rated players.)</p>
<h2>Final Goals</h2>
<p>This is going to be a great starting point for everyone that wants to start playing chess. People can get a lot of information that could help them improve faster.
And finally, the main point of this project is to defeat Magnus Carlsen.</p>
 
  

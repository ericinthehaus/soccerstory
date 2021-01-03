import cherrypy

index_html = """
<html>
<body>
<h1> Welcome to my soccer website!</h1>

    <form method="get" action=handle_names>
        Home team name: <br>
        <input type="text" name="home_name"><br>
        Away team name: <br>
        <input type="text" name="away_name"><br><br>
        <button type="submit">Enter!</button>
    </form>

"""

minutes_form_html = """
<html>
<body>
<p> which team leads at halftime? </p>
    <form action=handle_goal_data>
        <select name="min1_30" >
            <option value="home">Home</option>
            <option value="away">Away</option>
            <option value="tie" selected>Tied</option>
        </select><br>
<p> which team leads at the 75th minute? </p>
        <select name="min31_60" >
            <option value="home">Home</option>
            <option value="away">Away</option>
            <option value="tie" selected>Tied</option>
        </select>
         <br>
<p> which team won the game? </p>
        <select name="min61_90" >
            <option value="home">Home</option>
            <option value="away">Away</option>
            <option value="tie" selected>Tied</option>
        </select>
         <br><br> 
        <input type="submit" >
    </form>


</body>
</html>
"""

display_html = """
<html>
<body>
<h1> %s game performance: <br>

<canvas id="myCanvas" width="900" height="300"
style="border:3px solid #434443">
</canvas>

<script>

var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");

ctx.strokeStyle = "#308331";
ctx.lineWidth = 3;

ctx.moveTo(0,300);  
ctx.lineTo(150, 283.3);
ctx.lineTo(450, %f);
ctx.lineTo(750, %f);
ctx.lineTo(900,%d);

ctx.stroke();

</script>
<br>
<br>%s game performance: </h1> 

<canvas id="myCanvas2" width="900" height="300"
style="border:3px solid #434443">
</canvas>

<script>

var c2 = document.getElementById("myCanvas2");
var ctx2 = c2.getContext("2d");

ctx2.strokeStyle = "#d45751";
ctx2.lineWidth = 3;

ctx2.moveTo(0,300);  
ctx2.lineTo(150, 283.3);
ctx2.lineTo(450, %f);
ctx2.lineTo(750, %f);
ctx2.lineTo(900,%d);

ctx2.stroke();

</script>

</body>
</html>
"""

y1=200
y2=200
y3=200
home_list = [" "]
away_list = [" "]
z1=200
z2=200
z3=200
class LinesPrototypeWebApp:

    @cherrypy.expose
    def index(self):
        return index_html

    @cherrypy.expose
    def handle_names(self, home_name, away_name):
        home_list.append ( str (home_name) )
        away_list.append ( str (away_name) )
        return minutes_form_html

# y for home lines. z for away lines. 
    @cherrypy.expose
    def handle_goal_data(self, min1_30, min31_60, min61_90):
        if min1_30 == "home":
            y1= (283.3)*(0.6)
            z1= (2* (16.7)/3 ) + 283.3
        elif min1_30 == "away":
            y1= (2* (16.7)/3 ) + 283.3
            z1= (283.3)*(0.6)
        else:
            y1=250
            z1=250

        if min31_60 == "home":
            y2= y1*2 -(y1/450)*750
            z2= (2* (300-z1)/3 ) + z1
        elif min31_60 == "away":
            y2= (2* (300-y1)/3 ) + y1
            z2= z1*2 -(z1/450)*750
        else:
            y2=(2* (200-y1)/3 ) + y1
            z2=(2* (200-z1)/3 ) + z1

        if min61_90 == "home":
            y3=0
            z3=300
        elif min61_90 == "away":
            y3= 300
            z3=0
        else:
            y3=200
            z3=200
            
        return display_html % ( home_list[1], y1 , y2, y3,away_list[1], z1, z2, z3 )
            




our_app = LinesPrototypeWebApp()
static_file_config = {'/static': {'tools.staticdir.on': True, 'tools.staticdir.dir': '/home/ubuntu/teamXX/static'} }
cherrypy.quickstart(our_app, '/', static_file_config)

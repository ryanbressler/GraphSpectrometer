import scipy.io
import json
import sys

vispage = """<!DOCTYPE html>
<html>
    <head>
        <title>Information Content</title>
        <script src="http://d3js.org/d3.v2.js"></script>     
        <style>
            svg {
                border: solid 1px #ccc;
                font: 10px sans-serif;
                shape-rendering: crispEdges;
            }
        </style>             
    </head>
    <body>

        <div id="viz"></div>
        <div id="imp"></div>

        <script type="text/javascript">

            var matrix = %(json)s;

            var topImp = %(imp)s;

            var topClin = %(clinimp)s;

            var bottomls = ["F","M","NB","F","M","NB","F","M","NB","F","M","NB","F","M","NB","F","M","NB","F","M","NB","F","M","NB","F","M","NB","All"];
            var topls = ["ADMX","CLIN","DLTN","HHRF","HMST","MINA","MRGE","MTCD","SURV",""];

            var w = 1100,
            h = 300,
            imph = 360

            // create canvas
            var svg = d3.select("#viz").append("svg:svg")
            .attr("class", "chart")
            .attr("width", w)
            .attr("height", h )
            .append("svg:g")
            //.attr("transform", "translate(10,470)");

            
            y = d3.scale.linear().range([0, h-50])

        
            
            var rwidth = (w-50)/(matrix.length+3)
            console.log(matrix)

           

            x = function(i) {
            	return (i-1)*rwidth + Math.floor((i-1)/3)*10+10;
            }
            y.domain([0, 2]);

            svg.append("svg:line")
		        .attr("x1", 0)
		        .attr("y1", y(1))
		        .attr("x2", w)
		        .attr("y2", y(1))
		        .style("stroke", "rgb(220,220,220)")
		        .style("stroke-width", 8); 



            // Add a rect for each date.
            var rect = svg.selectAll("rect")
                .data(matrix)
                .enter()

            //upper rect
            rect.append("svg:rect")
                .attr("x", function(d,i) { return x(i+1); })
                .attr("y", function(d) { return y(2)-y(d[1])-y(d[2]); })
                .attr("height", function(d) { return y(d[1]); })
                .attr("fill","#FD8F42")
                .attr("stroke","#000000")
                .attr("width", rwidth);

            //lower rect
            rect.append("svg:rect")
                .attr("x", function(d,i) { return x(i+1); })
                .attr("y", function(d) { return y(2)-y(d[2]); })
                .attr("height", function(d) { return y(d[2]); })
                .attr("fill","#84ACBA")
                .attr("stroke","#000000")
                .attr("width", rwidth);
            
            var text = svg.selectAll("text")
                .data(matrix)
                .enter()

            text.append("svg:text")
                .attr("x", function(d,i) { return x(i+1)+2; })
                .attr("y", function(d) { return y(2)-y(d[1])-y(d[2])-4})
                .text( function (d) { return Math.round(50*(d[1]+d[2]))/100 || "" })
                .attr("font-family", "sans-serif")
                .attr("font-size", "12px")

            
            text.append("svg:text")
                .attr("x", function(d,i) { return x(i+1)+2; })
                .attr("y", function(d) { return y(2)-y(d[1])-y(d[2]) +12})
                .text( function (d) { return d[1] || "" })
                .attr("font-family", "sans-serif")
                .attr("font-size", "12px")

            text.append("svg:text")
                .attr("x", function(d,i) { return x(i+1)+2; })
                .attr("y", function(d) { return y(2)-y(d[2])+12; })
                .text( function (d) { return d[2] || "" })
                .attr("font-family", "sans-serif")
                .attr("font-size", "12px")

            text.append("svg:text")
                .attr("x", function(d,i) { return x(i+1)+8; })
                .attr("y", function(d) { return y(2)-4; })
                .text( function (d,i) { return bottomls[i] })
                .attr("font-family", "sans-serif")
                .attr("font-size", "12px")

            text.append("svg:text")
                .attr("x", function(d,i) { return x(i+1)+30; })
                .attr("y", function(d) { return y(2)+18; })
                .text( function (d,i) { return Math.floor(i/3)==i/3 ? topls[i/3] : ""; })
                .attr("font-family", "sans-serif")
                .attr("font-size", "12px");

            var imp = d3.select("#imp").append("svg:svg")
	            .attr("class", "chart")
	            .attr("width", w)
	            .attr("height", imph )
	            .append("svg:g");

	        var percol = 16;
	        var impx = function(i) {
	        	return i > (percol-1) ? w/2 : 0 + 10;
	        }

	        var impy = function(i) {
	        	less = i > (percol -1) ? percol : 0;
	        	return (i-less)*20 +30;
	        }

	        var impxscale = d3.scale.linear()
			     .domain([0, d3.max(topImp, function(d){return d[1];})])
			     .range([0, w/2-30]);

			imp.selectAll("rect")
				.data(topImp)
				.enter().append("rect")
				.attr("x", function(d,i){ return impx(i); })
				.attr("y", function(d, i) { return impy(i); })
				.attr("width", function(d) { return impxscale(d[1]); })
				.attr("height", 20)
				.attr("fill","#55bb55")
                .attr("stroke","#55bb55")

            var imptext = imp.selectAll("text")
                .data(topImp)
                .enter()

            imptext.append("svg:text")
                .attr("y", function(d, i) { return impy(i)+16; })
                .attr("x", function(d, i) { return impx(i) + 4; })
                .text( function (d) { return d[0]; })
                .attr("font-family", "sans-serif")
                .attr("font-size", "12px")

            imptext.append("svg:text")
                .attr("y", function(d, i) { return impy(i)+16; })
                .attr("x", function(d,i) { return impx(i)+impxscale(d[1])-30; })
                .text( function (d) { return Math.round(100*d[1])/100; })
                .attr("font-family", "sans-serif")
                .attr("font-size", "12px")

            imp.append("svg:text")
                .attr("y", 20)
                .attr("x", impx(1))
                .text( "CLIN, M" )
                .attr("font-family", "sans-serif")
                .attr("font-size", "12px")

            imp.append("svg:text")
                .attr("y", 20)
                .attr("x", impx(percol+1))
                .text( "All" )
                .attr("font-family", "sans-serif")
                .attr("font-size", "12px")




            




            


        </script>
    </body>
</html>
"""

def main():
    mat = scipy.io.loadmat(sys.argv[1])

    results = []

    #print mat["FIcell"][0]

    for i,v in enumerate(mat["CVcell"][0]):
    	if v.size == 4:
    		pre = 0.0
    		full = 0.0
    		try:
    			#pre = round(float(v[0][0])/float(v[0][0]+v[0][1]),2)
    			#full = round(float(v[1][0])/float(v[1][0]+v[1][1]),2)

    			pre = round(float(v[0][0])/(float(v[0][0])+float(v[1][0])),2)
    			full = round(float(v[1][1])/(float(v[0][1])+float(v[1][1])),2)
    		except:
    			pass
    		results.append([i+1, pre, full])
    	else:
    		results.append([i+1,0,0])

    imp = []
    clinimp = []

    for i,v in enumerate(mat["FIcell"][0][30][0]):
    	imp.append([v[0][0],mat["FIcell"][0][30][1][i][0]])
        clinimp.append([mat["FIcell"][0][4][0][i][0][0],mat["FIcell"][0][4][1][i][0]])

    #print mat["FIcell"][0]

    print vispage%{"json":json.dumps(results[:24]+results[27:]),"imp":json.dumps(clinimp[:16]+imp[:16]),"clinimp":json.dumps(clinimp[:16])}



if __name__ == '__main__':
	main()
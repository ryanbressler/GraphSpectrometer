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
                font: 10px Helvetica;
            }
        </style>             
    </head>
    <body>

        <div id="viz"></div>
        <div id="imp" ></div>
        <div id="prox"></div>

        <script type="text/javascript">

            var matrix = %(json)s;

            var topImp = %(imp)s;

            var topClin = %(clinimp)s;

            var leafdata = %(leafdata)s;

            // var bottomls = ["F","M","NB","F","M","F","M","NB","F","M","NB","F","M","NB","F","M","NB","F","M","NB","","M+F","","","NB","","F","M","All"];
            // var topls = ["Admixture","Clinical","Copy Number","Allele Type","Genomic Distance","Minor Allele Sum","Pathway","Merged Clinical","Mitochondrial","Survey",""];

            var bottomls = ["F","M","NB","F","M","NB","F","M","NB","F","M","NB","F","M","NB","F","M","NB","","NB","","F","M","","M+F","","F","M","All"];
            var topls = ["Admixture","Copy Number","Allele Type","Genomic Distance","Minor Allele Sum","Pathway","Mitochondrial","Clinical","Merged Clinical","Survey",""];

            var w = 1100,
                h = 180,
                imph = 240,
                percol = 10,
                proxh = 300

            // Predictive Power Bar Plot
            var svg = d3.select("#viz").append("svg:svg")
                .attr("class", "chart")
                .attr("width", w)
                .attr("height", h )
                .append("svg:g")

            var rwidth = (w-220)/(matrix.length+3)

            //hacky to get spacing right
            //i>4 is for cutting out clin newborn, 29 for cutting out survey newborn
            var x = function(i) {
                return (i-1)*rwidth + Math.floor((i-1+(i>21))/3)*20+(i>28)*20+80;
            }

            var y = d3.scale.linear().range([0, h-30])
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

            //balanced performance 
            text.append("svg:text")
                .attr("x", function(d,i) { return x(i+1)+rwidth/2; })
                .attr("text-anchor", "middle")
                .attr("y", function(d) { return y(2)-y(d[1])-y(d[2])-4})
                .text( function (d) { return Math.round(50*(d[1]+d[2]))/100 || "" })
                .attr("font-family", "Helvetica")
                .attr("font-size", "12px")

            //preterm 
            text.append("svg:text")
                .attr("x", function(d,i) { return x(i+1)+rwidth/2; })
                .attr("y", function(d) { return y(2)-y(d[1])-y(d[2]) +12})
                .attr("text-anchor", "middle")
                .text( function (d) { return d[1] || "" })
                .attr("font-family", "Helvetica")
                .attr("font-size", "12px")

            //fullterm
            text.append("svg:text")
                .attr("x", function(d,i) { return x(i+1)+rwidth/2; })
                .attr("y", function(d) { return y(2)-y(d[2])+12; })
                .attr("text-anchor", "middle")
                .text( function (d) { return d[2] || "" })
                .attr("font-family", "Helvetica")
                .attr("font-size", "12px")

            // M/F/NB labels
            text.append("svg:text")
                .attr("x", function(d,i) { return x(i+1)+rwidth/2; })
                .attr("y", function(d) { return y(2)-4; })
                .attr("text-anchor", "middle")
                .text( function (d,i) { return bottomls[i] })
                .attr("font-family", "Helvetica")
                .attr("font-size", "12px")

            //feature set label ... hack to get Survey to show up centered under two columns
            text.append("svg:text")
                .attr("x", function(d,i) { return x(i+1)+(3-(i==3||i>24))*rwidth/2; })
                .attr("y", function(d) { return y(2)+18; })
                .attr("text-anchor", "middle")
                .text( function (d,i) { i = i + (i>4); return Math.floor(i/3)==i/3 ? topls[i/3] : ""; })
                .attr("font-family", "Helvetica")
                .attr("font-size", "12px");
            //Legend

            //upper rect
            svg.append("svg:rect")
                .attr("x", 32)
                .attr("y", y(2)-y(.5)-y(.5))
                .attr("height", y(.5))
                .attr("fill","#FD8F42")
                .attr("stroke","#000000")
                .attr("width", rwidth);

            //lower rect
            svg.append("svg:rect")
                .attr("x", 32)
                .attr("y", y(2)-y(.5))
                .attr("height", y(.5))
                .attr("fill","#84ACBA")
                .attr("stroke","#000000")
                .attr("width", rwidth);

            svg.append("svg:text")
                .attr("x", 36)
                .attr("y", y(2)-y(.5)-y(.5)-4)
                .text( "Avg.")
                .attr("font-family", "Helvetica")
                .attr("font-size", "12px")

            
            svg.append("svg:text")
                .attr("x", 36)
                .attr("y", y(2)-y(.5)-y(.5) +12)
                .text( "Pre" )
                .attr("font-family", "Helvetica")
                .attr("font-size", "12px")

            svg.append("svg:text")
                .attr("x", 36)
                .attr("y", y(2)-y(.5)+12)
                .text( "Full" )
                .attr("font-family", "Helvetica")
                .attr("font-size", "12px")
             
            // Add a y-axis label.
            svg.append("text")
                .attr("class", "y label")
                .attr("text-anchor", "middle")
                .attr("y", 5)
                .attr("x", 0-(h/2))
                .attr("dy", ".75em")
                .attr("transform", "rotate(-90)")
                .text("Correct Classification Rate")
                .attr("font-family", "Helvetica")
                .attr("font-size", "12px");

            //title
            svg.append("text")
                .attr("class", "title")
                .attr("text-anchor", "middle")
                .attr("x", w/2)
                .attr("y", 16)
                .text("(a) Relative Pre/Fullterm Information Content of Feature Sets")
                .attr("font-family", "Helvetica")
                .attr("font-size", "13px")
                .attr("font-weight", "bold");

            /////////////////Importance Bar Plot (not shown at moment)

            var imp = d3.select("#imp").append("svg:svg")
                .attr("class", "chart")
                .attr("width", w)
                .attr("height", imph )
                .append("svg:g");

            
            var impx = function(i) {
                return i > (percol-1) ? w/2 : 0 + 10;
            }

            var impy = function(i) {
                less = i > (percol -1) ? percol : 0;
                return (i-less)*20 +30;
            }

            var impxscale = d3.scale.linear()
                 .domain([0, d3.max(topImp, function(d){return d[1];})])
                 .range([0, w/2-40]);

            var clinimpscale = d3.scale.linear()
                 .domain([0, d3.max(topClin, function(d){return d[1];})])
                 .range([0, w/2-40]);

            var impxscalefunc = function(x,i){ return i >= percol ? impxscale(x) : clinimpscale(x); }



            imp.selectAll("rect")
                .data(topImp)
                .enter().append("rect")
                .attr("x", function(d,i){ return impx(i); })
                .attr("y", function(d, i) { return impy(i); })
                .attr("width", function(d, i) { return impxscalefunc(d[1],i); })
                .attr("height", 20)
                .attr("fill","#00ee00")
                .attr("stroke","#000000")
                .style('stroke-opacity', 0.4)
                .style('fill-opacity', 0.4)

            var imptext = imp.selectAll("text")
                .data(topImp)
                .enter()

            imptext.append("svg:text")
                .attr("y", function(d, i) { return impy(i)+16; })
                .attr("x", function(d, i) { return impx(i) + 4; })
                .text( function (d) { return d[0]; })
                .attr("font-family", "Helvetica")
                .attr("font-size", "12px")

            imptext.append("svg:text")
                .attr("y", function(d, i) { return impy(i)+16; })
                .attr("x", function(d,i) { return impx(i)+impxscalefunc(d[1],i)-30; })
                .text( function (d) { return Math.round(100*d[1])/100; })
                .attr("font-family", "Helvetica")
                .attr("font-size", "12px")

            imp.append("svg:text")
                .attr("y", 20)
                .attr("x", impx(1))
                .text( "CLIN, M" )
                .attr("font-family", "Helvetica")
                .attr("font-size", "12px")

            imp.append("svg:text")
                .attr("y", 20)
                .attr("x", impx(percol+1))
                .text( "All" )
                .attr("font-family", "Helvetica")
                .attr("font-size", "12px")

            /////////////////// Proximity Scatter Plot

           /* var color = function(d) { return d[2] == "true" ? "#FD8F42" : "#84ACBA"; };

            var colors = ["#0000ff", "#D7191C", "#FDAE61", "#CCCCAC", "#ABD9E9", "#2C7BB6"];
          
            color = function(d){
                if ( ! colors.hasOwnProperty(parseInt(d[3]))){
                  console.log("bad color "+ (d[3]));
                  return "#000000";
                }
                return colors[d[3]];
            };*/

            var earliest = d3.min(leafdata, function(d){return d[4];});
            var latest = d3.max(leafdata, function(d){return d[4];})
            var colorscale = d3.scale.linear()
                 .domain([7*Math.floor(earliest/7),33*7,35*7,7*Math.ceil(latest/7) ])
                 .range(["#D7191C", "#FDAE61", "#CCCCAC", "#ABD9E9"]);
            color = function(d) {
                return colorscale(d[4]);
            }

            var proxx = d3.scale.linear()
                 .domain([d3.min(leafdata, function(d){return d[0];}), d3.max(leafdata, function(d){return d[0];})])
                 .range([0, w-50]);

            var proxy = d3.scale.linear()
                 .domain([d3.min(leafdata, function(d){return d[1];}), d3.max(leafdata, function(d){return d[1];})])
                 .range([0, proxh-60]);
            
            var proxsvg = d3.select("#prox")
                .append("svg")
                .attr("width", w)
                .attr("height", proxh);

            proxsvg.selectAll("circle")
                .data(leafdata)
                .enter()
                .append("circle")
                .attr("cx", function(d){ return proxx(d[0])+25; })
                .attr("cy", function(d){ return proxy(d[1])+30; })
                .attr("r", 6)
                .attr("fill",color)
                .attr("stroke",color)
                .style('stroke-opacity', 0.8)
                .style('fill-opacity', 0.8)
            //color Legend

            var colorLegend = [];
            for (var i = Math.floor(earliest/7); i <= Math.ceil(latest/7) ; i++) {
                colorLegend.push([i])
            }

            var xstart = 48

            proxsvg.selectAll("rect")
                .data(colorLegend)
                .enter()
                .append("rect")
                .attr("x", function(d,i){ console.log(i,d); return xstart + i*18; })
                .attr("y", proxh-17 )
                .attr("width", 18 )
                .attr("height", 14)
                .attr("fill", function(d){return colorscale(7*d[0]);})
                .attr("stroke",function(d){return colorscale(7*d[0]);})

            proxsvg.selectAll("text")
                .data(colorLegend)
                .enter().append("text")
                .attr("x", function(d,i){ console.log(i, d); return xstart + i*18 + 2; })
                .attr("y", proxh - 5 )
                .text(function(d){console.log(d); return ""+d[0];})
                .attr("font-family", "Helvetica")
                .attr("font-size", "12px");

            proxsvg.append("text")
                .attr("class", "colo label")
                .attr("x", xstart - 44)
                .attr("y", proxh - 5)
                .text("Weeks:")
                .attr("font-family", "Helvetica")
                .attr("font-size", "12px");

            // Add a y-axis label.
            proxsvg.append("text")
                .attr("class", "y label")
                .attr("text-anchor", "middle")
                .attr("y", 5)
                .attr("x", 0-(proxh/2))
                .attr("dy", ".75em")
                .attr("transform", "rotate(-90)")
                .text("Index in 2nd Eigenvector")
                .attr("font-family", "Helvetica")
                .attr("font-size", "12px");

            //x axis label
            proxsvg.append("text")
                .attr("class", "x label")
                .attr("text-anchor", "middle")
                .attr("x", w/2)
                .attr("y", proxh-5)
                .text("Index in 1st Eigenvector")
                .attr("font-family", "Helvetica")
                .attr("font-size", "12px");

            //title
            proxsvg.append("text")
                .attr("class", "title")
                .attr("text-anchor", "middle")
                .attr("x", w/2)
                .attr("y", 16)
                .text("(b) Family Proximity in Random Forest Learned From All Feature Sets Combined")
                .attr("font-family", "Helvetica")
                .attr("font-size", "13px")
                .attr("font-weight", "bold");
            

            


        </script>
    </body>
</html>
"""

def main():
    mat = scipy.io.loadmat(sys.argv[1]+"/results.mat")

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
    allimp = []
    
    for x in xrange(0,len(mat["FIcell"][0])):
        allimp.append([])
        fo = open(sys.argv[1]+"/topFs."+str(x)+".tsv","w")
        if len(mat["FIcell"][0][x])>0:
            for i,v in enumerate(mat["FIcell"][0][x][0]):
                if len(mat["FIcell"][0][x][1][i])>0:
                    allimp[-1].append([v[0][0],mat["FIcell"][0][x][1][i][0]])
                    fo.write("%s\t%s\n"%(v[0][0],mat["FIcell"][0][x][1][i][0]))
        fo.close()

    for i,v in enumerate(mat["FIcell"][0][33][0]):
    	imp.append([v[0][0],mat["FIcell"][0][33][1][i][0]])

    for i,v in enumerate(mat["FIcell"][0][4][0]):
        clinimp.append([v[0][0],mat["FIcell"][0][4][1][i][0]])

    leafdata = []
    #print mat["FIcell"][0]
    # fo = open(sys.argv[1]+"/leaffile.cutoff.0.0.json")
    # leafdata = json.load(fo)
    # fo.close()
    
    # leafdata = zip(leafdata["r1"],leafdata["r2"],leafdata["ptb"],leafdata["termcat"],leafdata["gestage"],leafdata["nByi"])

    #no qtl
    #results = results[:27]+results[30:]
    
    #no survey nb
    results = results[:29]+results[30:]
    
    merged = results[23]
    results[23]=results[22]
    results[22]=merged

    mitochonrial = results[26]
    results[26]=results[25]
    results[25]=mitochonrial

    #no clin nb
    results = results[:5]+results[6:]

    results = results[:3]+results[5:20]+results[23:26]+results[3:5]+results[20:23]+results[-3:]

    fo = open(sys.argv[1]+"/webdata.json","w")
    json.dump({"predpower":results, "leafdata":leafdata},fo)
    fo.close()



    print vispage%{"json":json.dumps(results),"imp":json.dumps(clinimp[:10]+imp[:10]),"clinimp":json.dumps(clinimp[:16]),"leafdata":json.dumps(leafdata)}



if __name__ == '__main__':
	main()
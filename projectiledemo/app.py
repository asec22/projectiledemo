from flask import Flask, render_template, Response, request,send_file
import numpy as np
import plotly.graph_objects as go

app = Flask(__name__)

def constants(x0,y0,theta,v0):
    v0st=str(v0)
    thetast=str(theta)
    ay=-9.81
    theta0=np.radians(theta)
    vx0=v0*np.cos(theta0)
    vy0=v0*np.sin(theta0)
    yrange=((vy0**2)/(2*-ay))+y0
    trange=(vy0/-ay)+(np.sqrt(((vy0/-ay)**2)+((2*y0)/-ay)))
    xrange=(trange*vx0)+x0
    return [v0st,ay,vx0,vy0,trange,xrange,yrange,thetast] 

def generate_plot(time,tmax,x1,x2,xi1,xi2,ymax,y1,y2,yi1,yi2,xmax,time_step):
    # make figure
    fig_dict = {
        "data":[],
        "layout": {},
        "frames": []
    }

    # fill in most of layout
    fig_dict["layout"]["xaxis"] = {"range": [0,xmax], "title": "X-Axis (m)"}
    fig_dict["layout"]["yaxis"] = {"range": [0,ymax], "title": "Y-Axis (m)"}
    fig_dict["layout"]["hovermode"] = "closest"
    fig_dict["layout"]["legend"]={"x":0.0, "y":1.2}
    fig_dict["layout"]["updatemenus"] = [
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 0, "redraw": False},
                                "fromcurrent": True, "transition": {"duration": (time_step*1000),
                                                                    "easing": "quadratic-in-out"}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                  "mode": "immediate",
                                  "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top"
        }
    ]

    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Time (s):",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": (time_step*1000), "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": []
    }
    j=0
    # make data
    for times in time:
        data_dict1 = {
            "x": x1,
            "y": y1,
            "mode":"lines",
            "line": {"width":2, "color":"blue"},
            "visible":True,
            "showlegend":False}
        data_dict2 = {
             "x": x2,
            "y": y2,
            "mode":"lines",
            "line": {"width":2, "color":"green"},
            "visible":True,
            "showlegend":False}                      
        fig_dict["data"].append(data_dict1)
        fig_dict["data"].append(data_dict2)                      
        j+=1


    # make frames
    k=0
    for times in time:
        frame = {"data": [], "name": str(round(times,2))}
        data_dict1 = {
                "x": [x1[k]],
                "y": [y1[k]],
                "mode": "markers",
                "marker": {"color":"blue", "size":10},
                "name": "Projectile (Velocity = "+path1[0]+" m/s, Angle = "+path1[7]+" degrees, launched at ("+str(xi1)+"m,"+str(yi1)+"m))",
                "showlegend":True}
        data_dict2 = {
                "x": [x2[k]],
                "y": [y2[k]],
                "mode": "markers",
                "marker": {"color":"green", "size":10},
                "name": "Projectile (Velocity = "+path2[0]+" m/s, Angle = "+path2[7]+" degrees, launched at ("+str(xi2)+"m,"+str(yi2)+"m))",
                "showlegend":True}                      
                          
        frame["data"].append(data_dict1)
        frame["data"].append(data_dict2)                      
    
    
        fig_dict["frames"].append(frame)
        k+=1
        slider_step = {"args": [
            [times],
            {"frame": {"duration": 0, "redraw": False},
             "mode": "immediate",
             "transition": {"duration": (time_step*1000) }}
        ],
            "label": str(round(times,2)),
            "method": "animate"}
        sliders_dict["steps"].append(slider_step)


    fig_dict["layout"]["sliders"] = [sliders_dict]

    fig = go.Figure(fig_dict)

    fig.write_html('static/projectile2.html')
    return fig
    
# Route to render the HTML page
@app.route('/', methods=["POST","GET"])
def index():
    return render_template('index8.html')

@app.route("/demo", methods=["POST", "GET"])
def demo():
    if request.method == "POST":
        xi1=float(request.form["xint1"])
        yi1=float(request.form["yint1"])
        vi1=float(request.form["velocity1"])
        thetai1=float(request.form["angle1"]) 
        xi2=float(request.form["xint2"])
        yi2=float(request.form["yint2"])
        vi2=float(request.form["velocity2"])
        thetai2=float(request.form["angle2"]) 
        
        global path1
        path1=constants(xi1,yi1,thetai1,vi1)
        global path2
        path2=constants(xi2,yi2,thetai2,vi2)
        
        trangelist=[path1[4],path2[4]]
        tmax=np.max(trangelist)                          
        xrangelist=[path1[5],path2[5]]
        xmax=np.max(xrangelist)                         
        yrangelist=[path1[6],path2[6]] 
        ymax=np.max(yrangelist)                          
                          
        time_step=round((tmax/100),2)
        time=np.arange(0.0,(tmax+time_step),time_step)
                          
        x1=(path1[2]*time)+xi1
        y1=((path1[1]*(time**2))/2)+(path1[3]*time)+yi1
                          
        x2=(path2[2]*time)+xi2
        y2=((path2[1]*(time**2))/2)+(path2[3]*time)+yi2 
        
        plot=generate_plot(time,tmax,x1,x2,xi1,xi2,ymax,y1,y2,yi1,yi2,xmax,time_step)
     
        return render_template("plot8.html")
    else:
        return render_template("index8.html")


    
# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True)

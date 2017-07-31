class Graph {
    constructor(name) {
        this.name = name;
        this.labels = {};
        this.svg = d3.select('#plot');
    }
}

Graph.prototype.register = function(label, option) {
    var href = '/get/' + label;
    if('interval' in option) {
        href += '/interval/' + option.interval;
    }
    else if('start' in option) {
        href += '/start/' + option.start;
        if('end' in option) {
            href += '/end/' + option.end;
        }
    }
    else if('end' in option) {
        href += '/end/' + option.end;
    }
    else if('count' in option) {
        href += '/count/' + option.count;
    }
    this.labels[label] = href;
}

Graph.prototype.ajax = function(callback) {
    var keys = Object.keys(this.labels)
    var ajax = [];
    for(var i=0; i<keys.length; i++) {
        ajax.push(axios.get(this.labels[keys[i]]));
    }
    axios.all(ajax)
        .then(axios.spread(callback));
}

Graph.prototype.init = function() {
    console.log("Please implement g.init() in /static/js/plot/" + this.name + ".js");
}

Graph.prototype.draw = function() {
    console.log("Please implement g.draw() in /static/js/plot/" + this.name + ".js");
}

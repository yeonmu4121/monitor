class Graph {
    constructor(name) {
        this.name = name;
    }
}

Graph.prototype.init = function() {
    console.log("Please implement g.init() in /static/js/plot/" + this.name + ".js");
}

Graph.prototype.draw = function() {
    console.log("Please implement g.draw() in /static/js/plot/" + this.name + ".js");
}

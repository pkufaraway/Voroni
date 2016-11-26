package VoronoiJava;

public class Point {
    int x,y;
    public static int distance(Point p1, Point p2){
        return Math.abs(p1.x - p2.x) + Math.abs(p1.y - p2.y);
    }

    public int distance (Point p2){
        return Math.abs(this.x - p2.x) + Math.abs(this.y - p2.y);
    }

    public Point move(Point move){
        return new Point(this.x + move.x, this.y + move.y);
    }

    public Point(int x, int y){
        this.x = x;
        this.y = y;
    }

    public Point(Point p){
        this.x = p.x;
        this.y = p.y;
    }

    @Override
    public String toString(){
        return String.valueOf(x) + " " + String.valueOf(y);
    }

    public boolean equals(Point p){
        return this.x == p.x && this.y == p.y;
    }

}

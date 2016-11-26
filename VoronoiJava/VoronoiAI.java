package VoronoiJava;

import java.util.DoubleSummaryStatistics;
import java.util.LinkedList;

class VoronoiAI{
    int numOfPlayers;
    int numOfStones;
    int role;
    LinkedList<Point> moves;
    double[][] data;
    int[][] choice;
    int[][] grid;
    int[][] smallChoice;

    double[][][] pull;
    double[][][] smallPull;


    public Point centerIndex(int x, int y){
        return new Point(x / 40, y / 40);
    }

    public Point realIndex(int x, int y){
        return new Point(x * 40 + 20, y * 40 + 20);
    }

    public double secondOfArray(double[] array, double max){
        double second = Double.MIN_VALUE;
        for(int i = 0; i < array.length; i++){
            if(array[i] > second && array[i] < max){
                second = array[i];
            }
        }
        return second;
    }

    private double sumOfArray(double[] array){
        double sum = 0;
        for(int i = 0; i < array.length; i++){
            sum += array[i];
        }
        return sum;
    }

    private double maxOfArray(double[] array){
        double max = Double.MIN_VALUE;
        for(int i = 0; i < array.length; i++){
            if(array[i] > max){
                max = array[i];
            }
        }
        return max;
    }

    public double distance(int x1,int y1, int x2, int y2){
        double distance = (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1);
        return Math.sqrt(distance);
    }

    public boolean isValid(int x, int y){
        for(Point p : moves){
            if(distance(x,y,p.x,p.y) < 66.0){
                return false;
            }
        }
        return true;
    }

    public boolean isValidCenter(Point c){
        for(int x = c.x - 20; x < c.x + 20; x++){
            for(int y = c.y - 20; y < c.y + 20; y++){
                boolean flag = true;
                for(Point p : moves){
                    if(distance(x,y,p.x,p.y) < 66.0){
                        flag = false;
                        break;
                    }
                }
                if(flag){
                    return true;
                }

            }
        }
        return false;
    }


    public VoronoiAI(int numOfPlayers, int numOfStones){
        this.numOfPlayers = numOfPlayers;
        this.numOfStones = numOfStones;
        this.grid = new int[1000][1000];
        this.choice = new int[1000][1000];
        this.smallChoice = new int[40][40];
        this.pull = new double[1000][1000][numOfPlayers + 1];
        this.smallPull = new double[40][40][numOfPlayers + 1];
        moves = new LinkedList<>();
    }

    public void newPull(int x, int y, int player){
        for(int i = 0; i < 1000; i++){
            for(int j = 0; j < 1000; j++){
                if(i != x || j != y) {
                    double score = 1.0 / ((i - x) * (i - x) + (j - y) * (j - y));
                    pull[i][j][player] += score;
                    Point center = centerIndex(i, j);
                    smallPull[center.x][center.y][player] += score;
                    if (pull[i][j][player] == maxOfArray(pull[i][j])) {
                        choice[i][j] = player;
                    }
                    if (smallPull[center.x][center.y][player] == maxOfArray(smallPull[center.x][center.y])) {
                        smallChoice[center.x][center.y] = player;
                    }
                }
            }
        }
    }

    public void newMove(int x, int y, int player){
        this.moves.add(new Point(x,y));
        newPull(x, y, player);
        grid[x][y] = player;
    }

    public void newMoves(String[] moves){
        int numOfMoves = Integer.valueOf(moves[1]);
        role = numOfMoves % numOfPlayers + 1;
        int start = numOfMoves - numOfPlayers + 1;
        if(start < 0){
            start = 0;
        }
        for(int i = start; i < numOfMoves; i++){
            int x = Integer.valueOf(moves[i * 3 + 2]);
            int y = Integer.valueOf(moves[i * 3 + 3]);
            int player = Integer.valueOf(moves[i * 3 + 4]);
            newMove(x, y, player);
        }
    }

    public double easyRefreshPull(Point point, int player) {
        int totalMoves = numOfStones * numOfPlayers;
        double finalValue = 0;
        for (int i = 0; i < 25; i++) {
            for (int j = 0; j < 25; j++) {
                Point real = realIndex(i, j);
                if (real.x != point.x || real.y != point.y) {
                    double score = 1.0 / ((real.x - point.x) * (real.x - point.x) + (real.y - point.y) * (real.y - point.y));
                    smallPull[i][j][player] += 1600 * score;
                    if (smallPull[i][j][player] == maxOfArray(smallPull[i][j])) {
                        if (moves.size() >= totalMoves * 2 / 3) {
                            finalValue += 1;
                        } else if (moves.size() >= totalMoves / 3) {
                            finalValue += smallPull[i][j][player] -
                                    (sumOfArray(smallPull[i][j]) - smallPull[i][j][player]) / (numOfStones - 1);
                        } else {
                            finalValue += smallPull[i][j][player] -
                                    secondOfArray(smallPull[i][j], smallPull[i][j][player]);
                        }
                    }
                    smallPull[i][j][player] -= 1600 * score;
                }
            }
        }
        return finalValue;
    }

    public String getMove(){
        if(role == 1 && moves.size() == 0){
            return "150 150";
        }
        double max = 0;
        Point result = new Point(0,0);
        for(int i = 0; i < 25; i++){
            for(int j = 0; j < 25; j++){
                Point center = realIndex(i,j);
                if(isValidCenter(center)) {
                    double score = easyRefreshPull(center, role);
                    if (score > max) {
                        max = score;
                        result = center;
                    }
                }

            }
        }

        int x = result.x;
        int y = result.y;
        max = 0;
        for(int i = x - 20; i < x + 20; i++){
            for(int j = y - 20; j < y + 20; j++){
                Point temp = new Point(i,j);
                if(isValid(i,j)) {
                    double score = easyRefreshPull(temp, role);
                    if (score > max) {
                        max = score;
                        result = temp;
                    }
                }

            }
        }

        newMove(result.x, result.y ,role);
        System.out.println(result.toString());
        return result.toString();
    }
}
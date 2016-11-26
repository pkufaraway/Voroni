package VoronoiJava;

import java.io.IOException;

public class GameRunner {

    public static void main(String[] args) throws IOException{
        int numStones = Integer.valueOf(args[0]);
        int numPlayers = Integer.valueOf(args[1]);
        int portNumber = Integer.valueOf(args[2]);
        GameController gameController = new GameController(numStones, numPlayers, portNumber);
    }

}

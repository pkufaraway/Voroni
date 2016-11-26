package VoronoiJava;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;

/*** Class that connects to a socket (5000 if the socket number is not defined
 * by the user), and reads the entire graph from the socket. You can get the
 * elements of the game from this class via getter methods. You can write your 
 * move to the server and the server will call the AI with the newest data
 * from the server.
 *
 * @author William Brantley
 *
 */
class GameController {
    private int portNumber;
    private int numPlayers;
    private int numStones;
    private Socket gameSocket;
    private PrintWriter outputStream;
    private BufferedReader inputStream;
    private VoronoiAI AI;

    GameController(int numStones, int numPlayers, int portNumber) throws IOException {
        this.portNumber = portNumber;
        this.numPlayers = numPlayers;
        this.numStones = numStones;
        AI = new VoronoiAI(numPlayers, numStones);
        connectToSocket();
        listenForMoves();
        endGame();
    }

    private void connectToSocket() {
        try {
            gameSocket = new Socket(InetAddress.getLocalHost(), this.portNumber);
            outputStream = new PrintWriter(gameSocket.getOutputStream(), true);
            inputStream = new BufferedReader(
                    new InputStreamReader(gameSocket.getInputStream()));
        } catch (Exception notHandled) {
            notHandled.printStackTrace();
        }
    }

    private void listenForMoves() throws IOException{
        while(true) {
            char[] incomingString;
            incomingString = new char[4096];
            inputStream.read(incomingString, 0, 4096);
            if (incomingString[0] == '1') {
                return;
            }
            String moves[] = new String(incomingString).trim().split(" ");
            AI.newMoves(moves);
            writeToSocket(AI.getMove());
        }
    }

    private void writeToSocket(String moveToMake) {
        outputStream.write(moveToMake);
        outputStream.flush();
    }

    private void endGame() throws IOException {
        outputStream.close();
        inputStream.close();
        gameSocket.close();
    }

}

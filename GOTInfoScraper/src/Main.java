import java.io.*;
import java.util.ArrayList;
import java.util.Scanner;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class Main {

    //episode descriptions
    //character descriptions
    //event descriptions
    //location descr
    //organization descr

    public static void main(String[] args) {


        Scanner in;
        try{
            in=new Scanner(new FileReader("..\\raw_data\\episode.csv"));
        }
        catch(Exception e){
            System.out.println("error reading file!");
            System.exit(1);
            return;
        }

        ArrayList<String> results=new ArrayList<String>();

        while(in.hasNextLine()){
            String linestr=in.nextLine();
            linestr=linestr.replaceAll(", ", "-");

            String[] line=linestr.split(",");
            line[1]="\""+line[1]+"\"";
            String episodeName=line[1];
            episodeName=episodeName.replaceAll("-",", ").replaceAll("\"","");

            System.out.println("Episode name: "+episodeName);

            Document document;
            try{
                document=Jsoup.connect("http://gameofthrones.wikia.com/wiki/"+episodeName).get();
            }
            catch(Exception ex){
                //System.err.println(e);
                System.out.println("getting page failed");
                return;
            }

            Element e;
            try{
                e=document.select("#Plot").get(0).parent();
            }
            catch (Exception ex){

                try{
                    document=Jsoup.connect("http://gameofthrones.wikia.com/wiki/"+episodeName+" (episode)").get();
                }
                catch(Exception exx){
                    //System.err.println(e);
                    System.out.println("getting page failed");
                    return;
                }

                e=document.select("#Plot").get(0).parent();

            }
            e=e.nextElementSibling();
            if(e.tagName().equals("figure")){
                e=e.nextElementSibling();
            }

            String plotDescription="";
            while(e.tagName().equals("p")){

                String s=e.html();
                String cleaned=s.replaceAll("<.*?>", "");
                plotDescription=plotDescription+cleaned+" ";
                e=e.nextElementSibling();
            }
            results.add(linestr+","+"\""+plotDescription+"\"");

        }


        //write to output

        String outputFileName="results.csv";


        File outFile = new File (outputFileName);
        FileWriter fWriter;
        try{
            fWriter = new FileWriter(outFile);
        }
        catch (IOException e){
            System.out.println("error writing file, quitting");
            return;
        }
        PrintWriter writer = new PrintWriter (fWriter);

        for(String s: results){
            writer.print(s+"\n");
        }
        writer.close();





    }



}

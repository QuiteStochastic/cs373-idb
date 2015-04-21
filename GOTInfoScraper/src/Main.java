import java.io.*;
import java.util.ArrayList;
import java.util.Scanner;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class Main {


    //character descriptions

    //organization descr

    public static void main(String[] args) {


        //scrapeForEpisodeDesc();

        //scrapeForLocationDesc();

        scrapeForCharacterDesc();

    }


    public static void scrapeForCharacterDesc(){
        Scanner in;
        try{
            in=new Scanner(new FileReader("..\\raw_data\\character.csv"));
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
            //line[1]="\""+line[1]+"\"";
            String charName=line[1]+"_"+line[2];

            System.out.println("Character name: "+charName);

            if(charName.equals("Hodor_Hodor")){
                continue;
            }



            Document document;
            try{
                document= Jsoup.connect("http://gameofthrones.wikia.com/wiki/" + charName).get();
            }
            catch(Exception ex){
                System.err.println(ex);
                System.out.println("getting page failed");
                return;
            }

            Element e;
            try{
                e=document.select(".quote").get(0);
            }
            catch (Exception ex){

                /*try{
                    document=Jsoup.connect("http://gameofthrones.wikia.com/wiki/"+locName+" (episode)").get();
                }
                catch(Exception exx){
                    //System.err.println(e);
                    System.out.println("second try, getting page failed");
                    return;
                }

                e=document.select("#Plot").get(0).parent();*/

                System.out.println("can't select right");
                return;

            }

            e=e.nextElementSibling();
/*            while(!e.tagName().equals("p")){
                e=e.nextElementSibling();
            }*/


            String charDescription="\"";


            while(e.tagName().equals("p")){

                String s=e.html();
                String cleaned=s.replaceAll("<.*?>", "");
                cleaned=cleaned.replaceAll("\\[.*?\\]", "");
                cleaned=cleaned.replaceAll("&nbsp;", " ");
                charDescription=charDescription+cleaned+" ";
                e=e.nextElementSibling();
            }

            charDescription=charDescription+"\"";
            System.out.println(charDescription);


            String toAdd=line[0]+","+line[1]+","+line[2]+line[3]+line[4]+line[5]+line[6]+","+"\""+charDescription+"\""+",";

            toAdd=toAdd+line[4]+",";

            results.add(toAdd);

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


    private static void scrapeForLocationDesc() {
        Scanner in;
        try{
            in=new Scanner(new FileReader("..\\raw_data\\location.csv"));
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
            //line[1]="\""+line[1]+"\"";
            String locName=line[1];

            System.out.println("Location name: "+locName);

            if(locName.equals("Essos") || locName.equals("Westeros")){
                String toAdd=line[0]+","+line[1]+","+line[2]+","+","+",";
                results.add(toAdd);

                continue;
            }

            Document document;
            try{
                document= Jsoup.connect("http://gameofthrones.wikia.com/wiki/" + locName).get();
            }
            catch(Exception ex){
                System.err.println(ex);
                System.out.println("getting page failed");
                return;
            }

            Element e;
            try{
                e=document.select("#mw-content-text").get(0).child(0);
            }
            catch (Exception ex){

                try{
                    document=Jsoup.connect("http://gameofthrones.wikia.com/wiki/"+locName+" (episode)").get();
                }
                catch(Exception exx){
                    //System.err.println(e);
                    System.out.println("second try, getting page failed");
                    return;
                }

                e=document.select("#Plot").get(0).parent();

            }
            //e=e.nextElementSibling();
            while(!e.tagName().equals("p")){
                e=e.nextElementSibling();
            }

            String s=e.html();
            String cleaned=s.replaceAll("<.*?>", "");
            cleaned=cleaned.replaceAll("\\[.*?\\]", "");
            String locDescription=cleaned+" ";

            System.out.println(locDescription);

            /*while(e.tagName().equals("p")){

                String s=e.html();
                String cleaned=s.replaceAll("<.*?>", "");
                plotDescription=plotDescription+cleaned+" ";
                e=e.nextElementSibling();
            }*/

            String toAdd=line[0]+","+line[1]+","+line[2]+","+"\""+locDescription+"\""+",";

            toAdd=toAdd+line[4]+",";

            results.add(toAdd);

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

    private static void scrapeForEpisodeDesc() {
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
                document= Jsoup.connect("http://gameofthrones.wikia.com/wiki/" + episodeName).get();
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

//package edu.nd.hci;
//
//import com.digitalpersona.uareu.Engine;
//import com.digitalpersona.uareu.Fmd;
//import com.digitalpersona.uareu.UareUException;
//import com.digitalpersona.uareu.UareUGlobal;
//
//import java.io.File;
//import java.io.FileInputStream;
//import java.util.ArrayList;
//
//public class Rollcall {
//
//    private String path;
//
//    public Rollcall(String path){
//        this.path = path;
//    }
//
//
//    // With code from https://stackoverflow.com/questions/14169661/read-complete-file-without-using-loop-in-java?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
//    // https://stackoverflow.com/questions/2102952/listing-files-in-a-directory-matching-a-pattern-in-java?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
//    public Fmd[] loadFingerprints() {
//        ArrayList<Fmd> prints = new ArrayList();
//        File dir = new File(path);
//        File[] files = dir.listFiles((d, name) -> name.endsWith(".fmd"));
//        for (File f: files) {
//            String ser;
//
//            try{
//
//                File file = new File("a.txt");
//                FileInputStream fis = new FileInputStream(file);
//                byte[] data = new byte[(int) file.length()];
//                fis.read(data);
//                fis.close();
//                ser = new String(data, "UTF-8");
//                Fmd print = Fmd.(ser);
//
//
//            } catch (Exception e){}
//
//        }
//
//    }
//
//    public void enroll(String id){
//        Engine engine = UareUGlobal.GetEngine();
//        try{
//            if(m_nFingerCnt > nIdx) m_fmds[nIdx] = engine.CreateFmd(evt.capture_result.image, Fmd.Format.ANSI_378_2004);
//            else fmdToIdentify = engine.CreateFmd(evt.capture_result.image, Fmd.Format.ANSI_378_2004);
//        }
//        catch(UareUException e){ MessageBox.DpError("Engine.CreateFmd()", e); }
//    }
//
//    public void identify(){
//
//
//        try{
//            //target false positive identification rate: 0.00001
//            //for a discussion of setting the threshold as well as the statistical validity of the dissimilarity score and error rates, consult the Developer Guide.
//            int falsepositive_rate = Engine.PROBABILITY_ONE / 100000;
//
//            Engine.Candidate[] vCandidates = engine.Identify(fmdToIdentify, 0, m_fmds, falsepositive_rate, m_nFingerCnt);
//
//            if(0 != vCandidates.length){
//                //optional: to get false match rate compare with the top candidate
//                int falsematch_rate = engine.Compare(fmdToIdentify, 0, m_fmds[vCandidates[0].fmd_index], vCandidates[0].view_index);
//
//                String str = String.format("Fingerprint identified, %s\n", m_vFingerNames[vCandidates[0].fmd_index]);
//                m_text.append(str);
//                str = String.format("dissimilarity score: 0x%x.\n", falsematch_rate);
//                m_text.append(str);
//                str = String.format("false match rate: %e.\n\n\n", (double)(falsematch_rate / Engine.PROBABILITY_ONE));
//                m_text.append(str);
//            }
//            else{
//                m_text.append("Fingerprint was not identified.\n\n\n");
//            }
//        } catch(UareUException e){ MessageBox.DpError("Engine.Identify()", e); }
//
//    }
//
//
//
//
//}

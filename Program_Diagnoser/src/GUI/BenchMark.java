package GUI;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.EventQueue;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JLabel;

import Experimenter.TDP_Run;
import Parsing.FilesAssist;
import Parsing.Method_Parser;

import javax.swing.AbstractButton;
import javax.swing.ImageIcon;
import javax.swing.JTabbedPane;
import javax.swing.JRadioButton;
import javax.swing.JButton;
import javax.swing.JFileChooser;

import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.io.File;
import java.io.IOException;
import java.nio.file.FileAlreadyExistsException;
import java.nio.file.FileSystems;
import java.util.Enumeration;
import java.awt.Font;

import javax.swing.ButtonGroup;
import javax.swing.JList;
import javax.swing.AbstractListModel;
import javax.swing.ListSelectionModel;
import javax.swing.border.LineBorder;
import javax.swing.JScrollPane;
import javax.swing.event.ListSelectionListener;
import javax.swing.event.ListSelectionEvent;
import javax.swing.JTextField;


public class BenchMark extends JFrame {

	private static final long serialVersionUID = -8872598972919543293L;
	

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		int iterations=Integer.parseInt(args[0]);
		String Instances=args[1];
		String out=args[2];
		FilesAssist.instances_path = 	 new File(Instances).toPath();
		FilesAssist.outPath = 	 new File(out).toPath().toString()+"\\";
		double threshold=Double.parseDouble(args[3]);
		
		//System.exit(0);
		//TDP_Run.executions_num=iterations;
		TDP_Run.set_executions_num(iterations);
		TDP_Run.set_threshold_prob(threshold);
		TDP_Run.set_init_tests(TDP_Run.initialize_method.BENCHMARK);
		TDP_Run.method_types selected = TDP_Run.method_types.values()[6];
		TDP_Run.set_plan_method(selected);
		try {
			TDP_Run.main(args);
		} catch (InterruptedException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
	}

	/**
	 * Create the frame.
	 */

	
	
	
	
}

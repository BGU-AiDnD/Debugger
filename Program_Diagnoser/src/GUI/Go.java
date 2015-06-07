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


public class Go extends JFrame {

	private static final long serialVersionUID = -8872598972919543293L;
	private JFileChooser fileChooser;
	private JPanel panel;
	private JTabbedPane tabbedPane;
	private ButtonGroup buttonGroup1 = new ButtonGroup();
	private ButtonGroup buttonGroup2 = new ButtonGroup();
	private JList<TDP_Run.method_types> list;
	private JTextField probText;
	private JTextField samplesText;
	private JTextField lookaheadText;
	private JTextField testsnoText;
	private JTextField execText;
	

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					Go frame = new Go();
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/**
	 * Create the frame.
	 */
	public Go() {
		setResizable(false);
		setTitle("TDP - Software MBD Experimenter");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 535, 388);
		getContentPane().setLayout(new BorderLayout(0, 0));
		
		tabbedPane = new JTabbedPane(JTabbedPane.TOP);
		getContentPane().add(tabbedPane);
		
		panel = new JPanel();
		tabbedPane.addTab("Basic Params", null, panel, null);
		panel.setLayout(null);
		
		JButton startExpbttn = new JButton("Start Experiment");
		startExpbttn.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				try {
					TDP_Run.set_executions_num(Integer.parseInt(execText.getText()));
					TDP_Run.main(null);
				} catch (InterruptedException | IOException e) {
					e.printStackTrace();
				}
			}
		});
		startExpbttn.setBounds(171, 295, 135, 23);
		panel.add(startExpbttn);
		
		JRadioButton rdbtnNewRadioButton_1 = new JRadioButton("Randomized Initial Tests");
		rdbtnNewRadioButton_1.setActionCommand("Random");
		rdbtnNewRadioButton_1.setSelected(true);
		rdbtnNewRadioButton_1.setBounds(31, 64, 177, 25);
		panel.add(rdbtnNewRadioButton_1);
		
		JRadioButton rdbtnNewRadioButton_2 = new JRadioButton("Run Benchmark");
		rdbtnNewRadioButton_2.setActionCommand("Benchmark");
		rdbtnNewRadioButton_2.setBounds(31, 93, 166, 25);
		panel.add(rdbtnNewRadioButton_2);
		
		//add listener to 1st class buttons
		radio1Listen radio_listener1 = new radio1Listen(); 
		rdbtnNewRadioButton_1.addActionListener(radio_listener1);
		rdbtnNewRadioButton_2.addActionListener(radio_listener1);
		
		//group the 1st class buttons
		buttonGroup1.add(rdbtnNewRadioButton_1);
		buttonGroup1.add(rdbtnNewRadioButton_2);

		
//////////////////////Add 2nd class radio buttons//////////////////////////////
		JRadioButton rdbtnBugs_1 = new JRadioButton("Randomize New Bugs");
		rdbtnBugs_1.setToolTipText("This option requires re-run of all tests!");
		rdbtnBugs_1.setActionCommand("RandNew");
		rdbtnBugs_1.setBounds(31, 185, 182, 30);
		panel.add(rdbtnBugs_1);
		
		JRadioButton rdbtnBugs_2 = new JRadioButton("Use Last Genetrated Bugs");
		rdbtnBugs_2.setActionCommand("TakeLast");
		rdbtnBugs_2.setSelected(true);
		rdbtnBugs_2.setBounds(31, 219, 192, 30);
		panel.add(rdbtnBugs_2);
		
		//group the 2nd class buttons
		buttonGroup2.add(rdbtnBugs_1);
		buttonGroup2.add(rdbtnBugs_2);
		
		//add listener to 2nd class buttons
		radio2Listen radio_listener2 = new radio2Listen(); 
		rdbtnBugs_1.addActionListener(radio_listener2);
		rdbtnBugs_2.addActionListener(radio_listener2);
		
		JLabel lblNewLabel = new JLabel("Choose Tests Initialization Method");
		lblNewLabel.setForeground(Color.BLUE);
		lblNewLabel.setFont(new Font("Arial", Font.BOLD, 13));
		lblNewLabel.setBounds(32, 39, 259, 17);
		panel.add(lblNewLabel);
		
		list = new JList<TDP_Run.method_types>();
		list.addListSelectionListener(new ListSelectionListener() {
			public void valueChanged(ListSelectionEvent e) {
				ListSelectionModel model = list.getSelectionModel();
				int index = model.getMaxSelectionIndex();
				TDP_Run.method_types selected = TDP_Run.method_types.values()[index];
				TDP_Run.set_plan_method(selected);
			}
		});
		list.setBorder(new LineBorder(new Color(0, 0, 0)));
		list.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
		list.setModel(new AbstractListModel<TDP_Run.method_types>() {
			private static final long serialVersionUID = 4814366336774195737L;
			TDP_Run.method_types[] values = TDP_Run.method_types.values();
			public int getSize() {
				return values.length;
			}
			public TDP_Run.method_types getElementAt(int index) {
				return values[index];
			}
		});
		list.setSelectedIndex(0);
		list.setBounds(334, 178, 52, -67);
		
		JScrollPane scrollPane = new JScrollPane();
		scrollPane.setBounds(317, 65, 121, 152);
		scrollPane.setViewportView(list);
		panel.add(scrollPane);
		
		JLabel lblChoosePlanTechnique = new JLabel("Choose Plan Technique");
		lblChoosePlanTechnique.setForeground(Color.BLUE);
		lblChoosePlanTechnique.setFont(new Font("Arial", Font.BOLD, 13));
		lblChoosePlanTechnique.setBounds(307, 39, 166, 17);
		panel.add(lblChoosePlanTechnique);
		
		JLabel lblChooseBugsSimulation = new JLabel("Choose Bugs Simulation Method");
		lblChooseBugsSimulation.setForeground(Color.BLUE);
		lblChooseBugsSimulation.setFont(new Font("Arial", Font.BOLD, 13));
		lblChooseBugsSimulation.setBounds(32, 160, 259, 17);
		panel.add(lblChooseBugsSimulation);
		
		//text listener
		TextListener textListener = new TextListener();
		
		//text field for Executions No.
		execText = new JTextField();
		execText.setToolTipText("Enter No. of executions.");
		execText.setText("" + TDP_Run.executions_num);
		execText.setColumns(5);
		execText.setBounds(453, 25, 59, 21);
		execText.addKeyListener(textListener);
		
		//insert image
		ImageIcon icon = new ImageIcon("icon.jpg");
		
		JPanel panel_1 = new JPanel();
		tabbedPane.addTab("Advanced Params", null, panel_1, null);
		panel_1.setLayout(null);
		
		JLabel label = new JLabel("Executions No.");
		label.setForeground(Color.BLUE);
		label.setFont(new Font("Arial", Font.BOLD, 13));
		label.setBounds(297, 27, 108, 17);
		panel_1.add(label);
		panel_1.add(execText);
		
		//text fields for MDP params
		probText = new JTextField();
		probText.setText("" + TDP_Run.threshold_prob);
		probText.setBounds(184, 25, 59, 21);
		panel_1.add(probText);
		probText.setColumns(5);
		probText.addKeyListener(textListener);
		
		samplesText = new JTextField();
		samplesText.setText("" + TDP_Run.samples);
		samplesText.setBounds(184, 71, 59, 21);
		panel_1.add(samplesText);
		samplesText.setColumns(2);
		samplesText.addKeyListener(textListener);
		
		lookaheadText = new JTextField();
		lookaheadText.setText("" + TDP_Run.lookahead);
		lookaheadText.setBounds(184, 116, 59, 21);
		panel_1.add(lookaheadText);
		lookaheadText.setColumns(2);
		lookaheadText.addKeyListener(textListener);
		
		testsnoText = new JTextField();
		testsnoText.setText("" + TDP_Run.initial_tests_num);
		testsnoText.setBounds(184, 161, 59, 21);
		panel_1.add(testsnoText);
		testsnoText.setColumns(3);
		testsnoText.addKeyListener(textListener);
		
		JLabel lblSamplesNo = new JLabel("Samples No.");
		lblSamplesNo.setForeground(Color.BLUE);
		lblSamplesNo.setFont(new Font("Arial", Font.BOLD, 13));
		lblSamplesNo.setBounds(12, 73, 108, 17);
		panel_1.add(lblSamplesNo);
		
		JLabel lblInitialTestsNo = new JLabel("Initial Tests No.");
		lblInitialTestsNo.setForeground(Color.BLUE);
		lblInitialTestsNo.setFont(new Font("Arial", Font.BOLD, 13));
		lblInitialTestsNo.setBounds(12, 163, 108, 17);
		panel_1.add(lblInitialTestsNo);
		
		JLabel lblLookahead = new JLabel("Lookahead");
		lblLookahead.setForeground(Color.BLUE);
		lblLookahead.setFont(new Font("Arial", Font.BOLD, 13));
		lblLookahead.setBounds(12, 118, 108, 17);
		panel_1.add(lblLookahead);
		
		JLabel lblThresholdProb = new JLabel("Threshold Prob.");
		lblThresholdProb.setForeground(Color.BLUE);
		lblThresholdProb.setFont(new Font("Arial", Font.BOLD, 13));
		lblThresholdProb.setBounds(12, 27, 108, 17);
		panel_1.add(lblThresholdProb);
		
		JButton btnNewButton_1 = new JButton("Apply");
		btnNewButton_1.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				TDP_Run.set_threshold_prob(Double.parseDouble(probText.getText()));
				TDP_Run.set_samples(Integer.parseInt(samplesText.getText()));
				TDP_Run.set_lookahead(Integer.parseInt(lookaheadText.getText()));
				TDP_Run.set_init_tests_num(Integer.parseInt(testsnoText.getText()));
				TDP_Run.set_executions_num(Integer.parseInt(execText.getText()));
			}
		});
		btnNewButton_1.setBounds(212, 229, 98, 27);
		panel_1.add(btnNewButton_1);
		
		JButton btnStartExperiment = new JButton("Start Experiment");
		btnStartExperiment.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try {
					TDP_Run.main(null);
				} catch (InterruptedException | IOException e1) {
					e1.printStackTrace();
				}
			}
		});
		btnStartExperiment.setBounds(194, 268, 141, 27);
		panel_1.add(btnStartExperiment);
		
		JLabel iconlabe2 = new JLabel(icon);
		iconlabe2.setText("");
		iconlabe2.setBounds(0, 192, 141, 118);
		panel_1.add(iconlabe2);
		
		JPanel panel_2 = new JPanel();
		tabbedPane.addTab("Tag Methods", null, panel_2, "A tool for hooking methods");
		panel_2.setLayout(null);
		
		fileChooser = new JFileChooser();
		fileChooser.setDialogType(1);
		fileChooser.setApproveButtonToolTipText("Tag all files in selected directory");
		fileChooser.setCurrentDirectory(FileSystems.getDefault().getPath("/").toFile());
		fileChooser.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				//handle OK button
				if (arg0.getActionCommand().equals("ApproveSelection")){
					File chosen_path = fileChooser.getSelectedFile();
					if (chosen_path == null)
						chosen_path = fileChooser.getCurrentDirectory();
					
					FilesAssist.set_source_path(chosen_path.toPath());
					
					try {
						File[] java_files = FilesAssist.get_all_java_files(); //gets relevant files
						Method_Parser.tag_methods(java_files);
						FilesAssist.plant_directory(); //handles the Implant directory creation
					} catch (IOException e) {
						e.printStackTrace();
					}
				}//end if
	
				//handle cancellation
				else if (arg0.getActionCommand().equals("CancelSelection"))
					tabbedPane.setSelectedIndex(0);
			}
		});
		
		JLabel lblChooseASource = new JLabel("Choose a source directory.");
		lblChooseASource.setForeground(Color.BLUE);
		lblChooseASource.setFont(new Font("Arial", Font.BOLD, 14));
		lblChooseASource.setBounds(10, 290, 207, 36);
		panel_2.add(lblChooseASource);
		fileChooser.setFileSelectionMode(1);
		fileChooser.setApproveButtonText("Tag");
		fileChooser.setBounds(0, 0, 500, 326);
		panel_2.add(fileChooser);
	}
	
	public ButtonGroup get_radi_group2(){
		return buttonGroup2;
	}
	
	class radio1Listen implements ActionListener{

		@Override
		public void actionPerformed(ActionEvent e) {
			Enumeration<AbstractButton> buttons = get_radi_group2().getElements();
			
			switch(e.getActionCommand()){
			case "Random":
				TDP_Run.set_init_tests(TDP_Run.initialize_method.RANDOM);
				while(buttons.hasMoreElements())
					buttons.nextElement().setEnabled(true);
				break;
			
			case "Benchmark":
				TDP_Run.set_init_tests(TDP_Run.initialize_method.BENCHMARK);
				while(buttons.hasMoreElements())
					buttons.nextElement().setEnabled(false);
				break;
			}
		}
	}//end class
	
	
	class radio2Listen implements ActionListener{

		@Override
		public void actionPerformed(ActionEvent e) {
			switch(e.getActionCommand()){
			case "RandNew":
				TDP_Run.set_bug_sim_mode(TDP_Run.bug_sim_mode.RANDOMIZE_NEW);
				break;
			
			case "TakeLast":
				TDP_Run.set_bug_sim_mode(TDP_Run.bug_sim_mode.TAKE_LAST);
				break;
			}
		}
	}//end class
	
	
	class TextListener implements KeyListener{

		@Override
		public void keyPressed(KeyEvent e) {
			if (e.getKeyCode() == 10){ //10 is the code for 'Enter'.
				TDP_Run.set_threshold_prob(Double.parseDouble(probText.getText()));
				TDP_Run.set_samples(Integer.parseInt(samplesText.getText()));
				TDP_Run.set_lookahead(Integer.parseInt(lookaheadText.getText()));
				TDP_Run.set_init_tests_num(Integer.parseInt(testsnoText.getText()));
				TDP_Run.set_executions_num(Integer.parseInt(execText.getText()));
			}//end if
		}

		@Override
		public void keyReleased(KeyEvent arg0) {
			//unimplemented
		}

		@Override
		public void keyTyped(KeyEvent arg0) {
			//unimplemented	
		}
	}//end class
}

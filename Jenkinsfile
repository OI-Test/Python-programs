pipeline {
    agent any
	/*
   environment{
	    	
	   	mail = sh(returnStdout: true, script: 'git --no-pager show -s --format=\'%ae\'').trim()
	   	//emails = sh(returnStdout: true, script: 'grep -E -o "\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.\[A-Za-z]{2,6}\b" Solutions/generator.py')
	   	line=sh(returnStdout: true, script: 'ls Solutions > files.txt | head -n 1 files.txt
			
	       } */	
    stages {
	    stage('Installing-Dependencies'){
	    	steps{
			sh'''
			sudo apt install -y python3-pip
			pip3 install --upgrade google-api-python-client --user
			pip3 install -r requirements.txt
			'''
		}
	    }
			    
	    stage('Tests') {
	    	steps {
			sh '''
			
			### CREATING A TEXT FILE W NAMES OF ALL FILES IN THE FOLDER AND REMOVING NON .PY ENTRIES FROM IT 
			ls Solutions > files.txt
			sed -i "/init/d" files.txt
			sed -i "/pycache/d" files.txt
			sed -i "/generator/d" files.txt
			
			
			
			### RENAMING ALL .PY FILES TO GENERATOR.PY ITERATIVELY FOR CONSISTENT TESTING. 
			while read lines;
			do  
			echo ${lines};
			cp Solutions/${lines} Solutions/generator.py
			
			
			
			### COVERAGE TESTS (COVERAGE MODULE)
			python3 -m coverage run Solutions/${lines}
			python3 -m coverage xml -o ./reports/${lines}_coverage.xml
			
			
			
			### UNIT TESTS (PYTEST MODULE)
			python3 -m pytest -v Tests/test.py --junit-xml reports/${lines}_testresults.xml
			
			
			
			### STYLE CHECKS (PYLINT MODULE)
			pylint --output-format=parseable --reports=no Solutions/${lines} > pylint.report || echo "pylint exited with $?"
			
			
			
			### CLEANING UP AND ENDING THE LOOP		
			rm Solutions/generator.py
			sed -i "1d" files.txt 
			done < files.txt
			echo "DONE"
			
			
			
			gpg --no-tty --passphrase oiuser004 --output $WORKSPACE/ \
			.git-crypt/keys/default/0/decrypted.gpg --decrypt $WORKSPACE/ \
			.git-crypt/keys/default/0/1C2F6666BCEE13ED19DB9A7EF20AC4CF9DEE46B7.gpg
			
			
			cat client_secret.json
			
			
			python3 send_mail.py -s abc@1.com -r trialacc911@gmail.com -t [TEST] -b hello
			
			'''
			
			
		    }
		
		post{ 
			always {
				// PYTEST AND PYLINT REPORT INTEGRATION (COBERTURA, WARNINGS-NG PLUGIN)
				junit allowEmptyResults: true, testResults: 'reports/*_testresults.xml'
				recordIssues(
                    			tool: pyLint(pattern: 'pylint.report'),
                    			unstableTotalAll: 20,
                    			failedTotalAll: 30
				)
				
				// SENDING EMAILS 
				emailext (
					subject: "FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'",
					body: """<p>FAILED: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]':</p>
						 <p>Check console output at &QUOT;<a href='${env.BUILD_URL}'>${env.JOB_NAME} [${env.BUILD_NUMBER}]</a>&QUOT;</p>""",
					//to: sh 'echo ${mails}',	
					    recipientProviders: [
								    //[$class: 'CulpritsRecipientProvider'],
								    [$class: 'DevelopersRecipientProvider'],
								    [$class: 'RequesterRecipientProvider']
								]
				    	)
				}
			}
		}
	}
}

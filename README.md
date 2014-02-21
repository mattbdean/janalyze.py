janalyze.py
===========

Ever wonder about the statistics of your project? How much of it is comments, documentation, whitespace, or code? This projects attempts to give you quick feedback on the makeup of one 

##Usage

```
# Analyze a file
./janalyze.py MyClass.java

# Analyze a whole folder
./janalyze.py src/
```

####Flags
```
-i, --individual  output the result for every file instead of one grand total. only applies if <target> is a directory.
-v, --verbose     shows the files that were analyzed
-d, --debug       shows debug information about file parsing
```

##Sample Output
```
me@my-computer:~/java-project$ janalyze.py src/SimpleClass.java
analyzer.py v1.0 by thatJavaNerd

SimpleClass.java

20 lines of code (64.52%)
 6 whitespace lines (19.35%)
 3 documentation lines (9.68%)
 2 comments (6.45%)
--------------
31 total lines
```

##Building the Test Project
The sample project used for testing is built with Gradle. You can build it by executing `./gradlew build` inside of the project directory.
```
cd java-test-project/
./gradlew build
```

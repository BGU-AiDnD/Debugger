__author__ = 'amir'

ONELINE_COMMENT_TOKEN = "//"
MULTILINE_COMMENT_TOKEN_BEGIN = "/*"
MULTILINE_COMMENT_TOKEN_END = "*/"


class Comment:
    def __init__(self):
        self.content = ""
        self.firstLineNumber = -1
        self.lastLineNumber = -1
        self.lines = []


    def addContent(self, appendedContent, lineNumber):
        self.content = " ".join([self.content, appendedContent])
        self.lastLineNumber = lineNumber
        self.lines.append(lineNumber)
        if self.firstLineNumber == -1:
            self.firstLineNumber = lineNumber


    def isEmpty(self):
        return self.firstLineNumber == -1


    def getContent(self):
        return self.content


    def getFirstLineNumber(self):
        return self.firstLineNumber


    def getLastLineNumber(self):
        return self.lastLineNumber


    def getLength(self):
        return self.getLastLineNumber() - self.getFirstLineNumber() + 1


    def newLine(self):
        self.content += "\n"


    def __str__(self):
        return "Comment from lines %d-%d:\n%s" %(self.getFirstLineNumber(),
            self.getLastLineNumber(), self.getContent())


class CommentFilter:
    def filterComments(self, source):
        """
            @input: list of lines of file
            @return: tuple containing list of lines of file and list of
                Comments
        """
        self.regularLines = []
        self.comments = []
        self.inMultilineComment = False
        self.currentComment = Comment()
        self.lineNumber = 0

        for line in source:
            self.currentLine = []
            while line:
                line = self.reduceLine(line)
            self.regularLines.append(" ".join(self.currentLine))
            self.lineNumber += 1
            if not self.currentComment.isEmpty():
                self.currentComment.newLine()

        if not self.currentComment.isEmpty():
            self.comments.append(self.currentComment)
            self.currentComment = Comment()

        return (self.regularLines, self.comments)


    def reduceLine(self, line):
        notInLine = 999999
        multiLineBeginPosition = notInLine
        multiLineEndPosition = notInLine
        oneLinePosition = notInLine

        if MULTILINE_COMMENT_TOKEN_BEGIN in line:
            multiLineBeginPosition = line.find(MULTILINE_COMMENT_TOKEN_BEGIN)

        if MULTILINE_COMMENT_TOKEN_END in line:
            multiLineEndPosition = line.find(MULTILINE_COMMENT_TOKEN_END)

        if ONELINE_COMMENT_TOKEN in line:
            oneLinePosition = line.find(ONELINE_COMMENT_TOKEN)

        if (not self.inMultilineComment
                and oneLinePosition < multiLineBeginPosition and len(line[:oneLinePosition].strip())!=0):
            self.currentLine.append(line[:oneLinePosition])
            self.currentComment.addContent(
                line[oneLinePosition + len(ONELINE_COMMENT_TOKEN):],
                self.lineNumber
            )
        elif self.inMultilineComment and multiLineEndPosition != notInLine:
            self.currentComment.addContent(
                line[:multiLineEndPosition],
                self.lineNumber
            )
            self.inMultilineComment = False
            return (line[multiLineEndPosition +
                len(MULTILINE_COMMENT_TOKEN_END):])
        elif multiLineBeginPosition != notInLine:
            self.currentLine.append(line[:multiLineBeginPosition])
            self.inMultilineComment = True
            return (line[multiLineBeginPosition +
                len(MULTILINE_COMMENT_TOKEN_BEGIN):])
        elif self.inMultilineComment:
            self.currentComment.addContent(line, self.lineNumber)
        else:
            if not self.currentComment.isEmpty():
                self.comments.append(self.currentComment)
                self.currentComment = Comment()
            self.currentLine.append(line)
        return ""


def commLines(path):
    with open(path, 'r') as f:
            source = f.read().splitlines()
            (regularLines, comments) = CommentFilter().filterComments(source)
            commentsLines=[]
            for c in comments:
                for x in c.lines:
                  commentsLines.append(x)
            return commentsLines

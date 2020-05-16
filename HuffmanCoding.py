import os
import heapq
class BinaryTreeNode:
    def __init__(self,value,frequency):
        self.value=value
        self.frequency=frequency
        self.left=None
        self.right=None
    def __lt__(self, other):
        return self.frequency<other.frequency
    def __eq__(self, other):
        return self.frequency==other.frequency

class HuffmanCoding:
    def __init__(self,path):
        self.path=path
        self.__heap=[]
        self.__codes={}
        self.__reverse_codes={}

    def _make_frequency_dict(self,text):
        freq_dict={}
        for char in text:
            if char not in freq_dict:
                freq_dict[char]=0
            freq_dict[char]+=1
        return freq_dict
    def __buildHeap(self,freq_dict):
        for key in freq_dict:
            frequency=freq_dict[key]
            binarytreenode=BinaryTreeNode(key,frequency)
            heapq.heappush(self.__heap,binarytreenode)
    def __buildTree(self):
        while len(self.__heap)>1:
            bt1=heapq.heappop(self.__heap)
            bt2=heapq.heappop(self.__heap)
            freq_sum=bt1.frequency+bt2.frequency
            newNode=BinaryTreeNode(None,freq_sum)
            newNode.left=bt1
            newNode.right=bt2
            heapq.heappush(self.__heap,newNode)
        return
    def __buildCodeHelper(self,root,curr_bits):
        if root is None:
            return
        if root.value is not None:
            self.__codes[root.value]=curr_bits
            self.__reverse_codes[curr_bits]=root.value
            return
        self.__buildCodeHelper(root.left,curr_bits+'1')
        self.__buildCodeHelper(root.right,curr_bits+'0')

    def __buildcodes(self):
        if len(self.__heap)>0:
            root=heapq.heappop(self.__heap)
            self.__buildCodeHelper(root,'')
    def __getEncodedText(self,text):
        encoded_text=''
        for char in text:
            encoded_text+=self.__codes[char]
        return encoded_text
    def __getPaddedText(self,encoded_text):
        padded_amount=8-len(encoded_text)%8
        for i in range(padded_amount):
            encoded_text+='0'
        padded_info='{0:08b}'.format(padded_amount)
        encoded_text=padded_info+encoded_text
        return encoded_text
    def __getByteArray(self,padded_encoded_text):
        array=[]
        for i in range(0,len(padded_encoded_text),8):
            byte=padded_encoded_text[i:i+8]
            array.append(int(byte,2))
        return array


    def compress(self):
        file_name,file_extension=os.path.splitext(self.path)
        output_path=file_name+'.bin'
        with open(self.path,'r+') as file,open(output_path,'wb') as output:
            text=file.read()
            text=text.rstrip()
            freq_dict = self._make_frequency_dict(text)
            self.__buildHeap(freq_dict)
            self.__buildTree()
            self.__buildcodes()
            encoded_texts=self.__getEncodedText(text)
            padded_encoded_text=self.__getPaddedText(encoded_texts)
            bytes_array=self.__getByteArray(padded_encoded_text)
            final_bytes=bytes(bytes_array)
            output.write(final_bytes)
        print('File compressed and saved')
        print(final_bytes)
        return output_path
    def __removePadding(self,bit_string):
        padded_info=bit_string[:8]
        extra_padding=int(padded_info,2)
        bit_string=bit_string[8:]
        text_after=bit_string[:-1*extra_padding]
        return text_after
    def __decode_texts(self,text):
        decoded_text=''
        current_bits=''
        for bit in text:
            current_bits+=bit
            if current_bits in self.__reverse_codes:
                character=self.__reverse_codes[current_bits]
                decoded_text+=character
                current_bits=''
        return decoded_text
    def decompress(self,input_path):
        file_name,file_extension=os.path.splitext(self.path)
        output_path=file_name+'_decompressed'+'.txt'
        with open(input_path,'rb') as file,open(output_path,'w') as output:
            bit_string=''
            byte=file.read(1)
            while byte:
                byte=ord(byte)
                bits=bin(byte)[2:].rjust(8,'0')
                bit_string+=bits
                byte=file.read(1)
            actual_text=self.__removePadding(bit_string)
            decompressed_text=self.__decode_texts(actual_text)
            output.write(decompressed_text)
            print('File Decompressed')
        return

path='C:/Users/VIPUL/Desktop/sample1.txt'

h=HuffmanCoding(path)
output_path=h.compress()
h.decompress(output_path)


#! /usr/bin/python
# -*- coding:utf-8 -*-
generation_list = []

class Generation(object):
	"""docstring for generation"""
	def __init__(self):
		super(Generation, self).__init__()
		self.key = ''
		self.values_list = []


def add_generation(key, a_right_value, b_right_value):
	behind_str = '_x'
	pre_generation = Generation()
	after_generation = Generation()
	pre_generation.key = key
	after_key = key + behind_str
	after_generation.key = after_key
	for item in b_right_value:
		pre_generation.values_list.append(after_key+' '+item)
	for item in a_right_value:
		after_generation.values_list.append(item)
	after_generation.values_list.append('@')
	generation_list.append(pre_generation)
	generation_list.append(after_generation)



def remove_left_recursive():
	for generation_item in generation_list:
		a_right_value = []
		b_right_value = []
		left_recursive_flag = False
		for value in generation_item.values_list:
			item = value.split(' ')
			if generation_item.key == item[0]:
				left_recursive_flag = True
				if len(item)>1:
					output_str = ''
					tmp_item = item[1:]
					for word in tmp_item:
						output_str += (word+' ')
					a_right_value.append(output_str)
			else:
				output_str = ''
				for word in item:
					output_str += (word+' ')
				b_right_value.append(output_str)
		if left_recursive_flag:
			key = generation_item.key
			generation_list.remove(generation_item)
			add_generation(key,a_right_value,b_right_value)


def display():
	fileout = open('out_grammer.txt', 'w')
	for generation_item in generation_list:
		for item in generation_item.values_list:
			fileout.write(generation_item.key+' '+item+'\n')



def main():
	filein = open('grammer.txt', 'r')
	key_value_flag = True
	while True:
		line = filein.readline()
		if not line:
			break
		line = line.strip('\t')
		if line == '\n':
			continue
		line = line.rstrip('\n')
		if line[0] == ';':
			generation_list.append(tmp_generation)
			key_value_flag = True
		if line[0] == ':':
			key_value_flag = False
		if key_value_flag:
			tmp_generation = Generation()
			tmp_generation.key = line
		else:
			line = line[1:]
			line = line.lstrip()
			#print(line)
			#print(len(tmp_generation.values_list))
			tmp_generation.values_list.append(line)
	remove_left_recursive()
	display()



if __name__ == '__main__':
	main()
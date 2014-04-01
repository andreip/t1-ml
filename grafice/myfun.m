function [X] = myfun(v)

X = []
step = 100
for i = step:step:length(v)
	X = [X, mean(v(i-step+1:i))];
endfor;

end;

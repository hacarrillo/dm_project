M = csvread('filteredUserAnimeList.csv',1,3,[1,3,40000000,3]);
gt = dlmread('gt.txt');
missed = dlmread('resultsAnimeMissed.txt');

s = 336233;
gt = gt(1:s);

[h,w] = size(gt);
counts_gt = hist(gt,.5:1:9.5);
percent_gt = counts_gt./h;

[h,w] = size(M);
counts_all = hist(M, .5:1:9.5);
percent_all = counts_all./h
cpd_all = [];

c = 0;
for i=1:10
    c = c + percent_all(i);
    cpd_all = [cpd_all, c];
end
cpd_all

pred = zeros(s,1);

for i=1:s
    p = rand;
    p = sum(cpd_all < p);
    pred(i) = p;
end

difference = abs(pred-gt);
counts = hist(difference,0:10);
counts_percent = 100*counts./s;
figure
scatter(0:10,counts_percent,'filled');
ylabel('Percentage')
title('Prediction VS Ground Truth Distribution for random guess')
xlabel('|predicted - ground truth|')

c = 0;
cpd = [];
for i=1:11
    c = c + counts_percent(i);
    cpd = [cpd, c];
end

figure
scatter(0:10,cpd,'filled');
ylabel('Percentage')
title('Prediction VS Ground Truth Distribution Cumulative Probability Distribution for random guess')
xlabel('|predicted - ground truth|')

counts = hist(missed,0:10);
counts_percent = 100*counts./s;
figure
scatter(0:10,counts_percent,'filled');
ylabel('Percentage')
title('Prediction VS Ground Truth Distribution for CBCF')
xlabel('|predicted - ground truth|')

c = 0;
cpd_cbcf = [];
for i=1:11
    c = c + counts_percent(i);
    cpd_cbcf = [cpd_cbcf, c];
end

figure
scatter(0:10,cpd_cbcf,'filled');
ylabel('Percentage')
title('Prediction VS Ground Truth Distribution Cumulative Probability Distribution for CBCF')
xlabel('|predicted - ground truth|')

figure 
scatter(0:10,cpd_cbcf,'filled');
hold on 
scatter(0:10,cpd,'filled');
ylabel('Percentage')
title('Prediction VS Ground Truth Distribution Cumulative Probability Comparison')
xlabel('|predicted - ground truth|')
legend('CBCF','Random Guess');

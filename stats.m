M = csvread('filteredUserAnimeList.csv',1,3,[1,3,40000000,3]);

histogram(M)
xlabel('Score');
ylabel('Count');
title('Histogram of Review Scores');






# Final Results 
## CRF Comparison
![crf_all_comparison_20_80_set_features_pos](https://user-images.githubusercontent.com/71148152/185637515-7a00e128-e8f2-4d29-a0bb-2fbfd22d5227.png)

Different groupings of CRF training sets perform similarly to each other. 

## NLP Benchmark Comparison
![benchmark_with_crf_20_80_set_features_pos](https://user-images.githubusercontent.com/71148152/185641370-6354b65f-a2c4-49f0-a6ba-d85507668a5f.png)
<p align="center" > <em>  The above CRF results used features that mainly depend on POS tags </em> </p> 

CRF NLP performs better than the other NLP tools' annotation in all categories and label types. ECMFA-VN and Visual Narrator performs about the same or worse than the Simple NLP. This implies that these two NLP's calculations are redundant. 

<h3 align="center" > <strong>  NLP Benchmark Comparison Data </strong> </h3> 
<img width="1100" alt="20_80_features_pos" src="https://user-images.githubusercontent.com/71148152/185648983-f6f14e07-8cab-4fe3-b16d-983f23e71d46.png">
   
## NLP Primary Results Benchmark Comparison
![primary_benchmark_with_crf_20_80_set_features_pos](https://user-images.githubusercontent.com/71148152/185641510-cbe88c8a-71b5-4b17-a0c1-77963824f8f1.png)
<p align="center" > <em>  The above CRF results used features that mainly depend on POS tags </em> </p> 

<h3 align="center" > <strong>  Primary Results NLP Benchmark Comparison Data </strong> </h3> 
<img width="1100" alt="20_80_primary" src="https://user-images.githubusercontent.com/71148152/185653102-cd683339-c1ef-4bfc-b22a-3aae9200aba1.png">

## Note
CRF models must be trained using different sets of features based on the size of the training set. Larger training sets become dependent on specific words learned. Word dependencies make it difficult to scale CRF models when attempting to evaluate a different dataset. A set of features that mainly depends on POS tags was developed to solve this issue. The final CRF results that used the POS features only dropped their f-measure score by no more than 0.05. Also, these results still performed better than the other NLP tools' annotations. 

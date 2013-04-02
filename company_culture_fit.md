Company culture fit
===================

Where do I fit in compared to your employees linkedin.com profiles?

Getting the data
----------------

### Linkedin.com parser

First we import a parser and some small helper functions for linkedin public profiles:

<div class="highlight"><pre><span class="kn">from</span> <span class="nn">linkedin</span> <span class="kn">import</span> <span class="n">linkedin_parser</span> <span class="k">as</span> <span class="n">lp</span>
<span class="kn">from</span> <span class="nn">linkedin</span> <span class="kn">import</span> <span class="n">linkedin_helpers</span> <span class="k">as</span> <span class="n">lh</span>
</pre></div>



### List of employees

Let's make a list of employees with at least a resonably complete linkedin.com profile page:

<div class="highlight"><pre><span class="kn">from</span> <span class="nn">employee_data</span> <span class="kn">import</span> <span class="n">redfin</span> <span class="k">as</span> <span class="n">rf</span>
<span class="kn">from</span> <span class="nn">employee_data</span> <span class="kn">import</span> <span class="n">climate_corp</span> <span class="k">as</span> <span class="n">cc</span>
<span class="kn">from</span> <span class="nn">employee_data</span> <span class="kn">import</span> <span class="n">simply_measured</span> <span class="k">as</span> <span class="n">sm</span>
<span class="kn">from</span> <span class="nn">employee_data</span> <span class="kn">import</span> <span class="n">random_people</span> <span class="k">as</span> <span class="n">rd</span>
</pre></div>



For example, here are some redfin people and their urls:

<div class="highlight"><pre><span class="nb">zip</span><span class="p">(</span><span class="n">rf</span><span class="o">.</span><span class="n">redfin_people</span><span class="p">,</span> <span class="n">rf</span><span class="o">.</span><span class="n">redfin_urls</span><span class="p">)[</span><span class="mi">0</span><span class="p">:</span><span class="mi">5</span><span class="p">]</span>
</pre></div>


<pre>
    [('Mark Carr', 'http://www.linkedin.com/in/markcarr'),
     ('Jim Lamb', 'http://www.linkedin.com/in/jimplamb'),
     ('Krystin Tate', 'http://www.linkedin.com/in/krystin'),
     ('Andy Taylor', 'http://www.linkedin.com/in/andyataylor'),
     ('Taylor Connolly', 'http://www.linkedin.com/in/taylorconnolly')]
</pre>


### Creating the corpus:

Pick the companies we want to analyize and write the words used in the linkedin.com profile into a text file of features:

<div class="highlight"><pre><span class="n">my_url</span> <span class="o">=</span> <span class="p">[</span><span class="s">&#39;http://www.linkedin.com/in/dleen&#39;</span><span class="p">]</span>
<span class="n">company_urls</span> <span class="o">=</span> <span class="p">[</span><span class="n">my_url</span><span class="p">,</span>
                <span class="n">rf</span><span class="o">.</span><span class="n">redfin_urls</span><span class="p">,</span>
                <span class="n">cc</span><span class="o">.</span><span class="n">climate_corp_urls</span><span class="p">,</span>
                <span class="n">sm</span><span class="o">.</span><span class="n">simply_measured_urls</span><span class="p">,</span>
                <span class="n">rd</span><span class="o">.</span><span class="n">random_urls</span>
                <span class="p">]</span>  

<span class="n">file_name</span> <span class="o">=</span> <span class="s">&#39;people.txt&#39;</span>

<span class="k">try</span><span class="p">:</span>
    <span class="k">with</span> <span class="nb">open</span><span class="p">(</span><span class="n">file_name</span><span class="p">):</span> <span class="k">print</span><span class="p">(</span><span class="s">&quot;File exists! Don&#39;t do anything.&quot;</span><span class="p">)</span>
<span class="k">except</span> <span class="ne">IOError</span><span class="p">:</span>
    <span class="k">print</span><span class="p">(</span><span class="s">&quot;Writing the corpus (may take a few minutes)&quot;</span><span class="p">)</span>
    <span class="k">with</span> <span class="nb">open</span><span class="p">(</span><span class="n">file_name</span><span class="p">,</span> <span class="s">&#39;w&#39;</span><span class="p">)</span> <span class="k">as</span> <span class="n">f</span><span class="p">:</span>
        <span class="k">for</span> <span class="n">i</span><span class="p">,</span> <span class="n">u</span> <span class="ow">in</span> <span class="nb">enumerate</span><span class="p">(</span><span class="n">company_urls</span><span class="p">,</span> <span class="n">start</span><span class="o">=</span><span class="mi">0</span><span class="p">):</span>
            <span class="n">lh</span><span class="o">.</span><span class="n">write_linkedin_data</span><span class="p">(</span><span class="n">f</span><span class="p">,</span> <span class="n">i</span><span class="p">,</span> <span class="n">u</span><span class="p">)</span>
    

<span class="kn">from</span> <span class="nn">IPython.core.display</span> <span class="kn">import</span> <span class="n">clear_output</span>
<span class="n">clear_output</span><span class="p">()</span>
</pre></div>



Analyzing the employees
-----------------------

### Tfidf

<div class="highlight"><pre><span class="kn">from</span> <span class="nn">sklearn.feature_extraction.text</span> <span class="kn">import</span> <span class="n">TfidfVectorizer</span>

<span class="k">with</span> <span class="nb">open</span><span class="p">(</span><span class="n">file_name</span><span class="p">,</span> <span class="s">&#39;r&#39;</span><span class="p">)</span> <span class="k">as</span> <span class="n">f</span><span class="p">:</span>
    <span class="n">corpus</span> <span class="o">=</span> <span class="p">[]</span>
    <span class="n">labels</span> <span class="o">=</span> <span class="p">[]</span>
    <span class="k">for</span> <span class="n">line</span> <span class="ow">in</span> <span class="n">f</span><span class="p">:</span>
        <span class="n">labels</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="nb">int</span><span class="p">(</span><span class="n">line</span><span class="p">[</span><span class="mi">0</span><span class="p">]))</span>
        <span class="n">corpus</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">line</span><span class="p">[</span><span class="mi">2</span><span class="p">:])</span>
        
<span class="n">vectorizer</span> <span class="o">=</span> <span class="n">TfidfVectorizer</span><span class="p">(</span><span class="n">min_df</span><span class="o">=</span><span class="mi">1</span><span class="p">)</span>
<span class="n">tfidf</span> <span class="o">=</span> <span class="n">vectorizer</span><span class="o">.</span><span class="n">fit_transform</span><span class="p">(</span><span class="n">corpus</span><span class="p">)</span>
<span class="n">feature_names</span> <span class="o">=</span> <span class="n">vectorizer</span><span class="o">.</span><span class="n">get_feature_names</span><span class="p">()</span>
<span class="n">labels</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">(</span><span class="n">labels</span><span class="p">)</span> 
</pre></div>



<div class="highlight"><pre><span class="kn">import</span> <span class="nn">itertools</span>

<span class="n">a</span> <span class="o">=</span> <span class="n">itertools</span><span class="o">.</span><span class="n">izip</span><span class="p">(</span><span class="n">feature_names</span><span class="p">,</span> <span class="n">tfidf</span><span class="o">.</span><span class="n">data</span><span class="p">)</span>
<span class="n">b</span> <span class="o">=</span> <span class="nb">sorted</span><span class="p">(</span><span class="n">a</span><span class="p">,</span> <span class="n">key</span><span class="o">=</span><span class="k">lambda</span> <span class="n">x</span><span class="p">:</span> <span class="n">x</span><span class="p">[</span><span class="mi">1</span><span class="p">],</span> <span class="n">reverse</span><span class="o">=</span><span class="bp">True</span><span class="p">)</span> 
<span class="k">print</span> <span class="n">b</span><span class="p">[:</span><span class="mi">5</span><span class="p">]</span>
</pre></div>


    [(u'strings', 0.67608006133504683), (u'beyond', 0.51467175149098765), (u'teggart', 0.49532011897004113), (u'quarterly', 0.47901679669287373), (u'subjects', 0.47320852663699264)]


### PCA

<div class="highlight"><pre><span class="kn">from</span> <span class="nn">sklearn.decomposition</span> <span class="kn">import</span> <span class="n">PCA</span>

<span class="n">pca</span> <span class="o">=</span> <span class="n">PCA</span><span class="p">(</span><span class="n">n_components</span><span class="o">=</span><span class="mi">2</span><span class="p">)</span>
<span class="n">reduced_data</span> <span class="o">=</span> <span class="n">pca</span><span class="o">.</span><span class="n">fit_transform</span><span class="p">(</span><span class="n">tfidf</span><span class="o">.</span><span class="n">toarray</span><span class="p">())</span>

<span class="n">reduced_data</span><span class="p">[</span><span class="mi">0</span><span class="p">:</span><span class="mi">5</span><span class="p">]</span>
</pre></div>


<pre>
    array([[-0.07764109,  0.04700812],
           [ 0.08787915, -0.29793791],
           [-0.18104213, -0.43717093],
           [ 0.1544524 , -0.29056254],
           [-0.21848148, -0.26427421]])
</pre>


### k-Means

<div class="highlight"><pre><span class="kn">from</span> <span class="nn">sklearn.cluster</span> <span class="kn">import</span> <span class="n">KMeans</span>

<span class="n">kmeans</span> <span class="o">=</span> <span class="n">KMeans</span><span class="p">(</span><span class="n">init</span><span class="o">=</span><span class="s">&#39;k-means++&#39;</span><span class="p">,</span> <span class="n">n_clusters</span><span class="o">=</span><span class="mi">4</span><span class="p">)</span>
<span class="n">kmeans</span><span class="o">.</span><span class="n">fit</span><span class="p">(</span><span class="n">reduced_data</span><span class="p">[</span><span class="mi">1</span><span class="p">:])</span>
</pre></div>


<pre>
    KMeans(copy_x=True, init='k-means++', k=None, max_iter=300, n_clusters=4,
        n_init=10, n_jobs=1, precompute_distances=True, random_state=None,
        tol=0.0001, verbose=0)
</pre>


Visualizing the data
--------------------

### Make a grid

<div class="highlight"><pre><span class="c"># Step size of the mesh. Decrease to increase the quality of the VQ.</span>
<span class="n">h</span> <span class="o">=</span> <span class="mf">0.01</span>     <span class="c"># point in the mesh [x_min, m_max]x[y_min, y_max].</span>

<span class="c"># Plot the decision boundary. For that, we will asign a color to each</span>
<span class="n">x_min</span><span class="p">,</span> <span class="n">x_max</span> <span class="o">=</span> <span class="n">reduced_data</span><span class="p">[:,</span> <span class="mi">0</span><span class="p">]</span><span class="o">.</span><span class="n">min</span><span class="p">()</span> <span class="o">-</span> <span class="mf">0.1</span><span class="p">,</span> <span class="n">reduced_data</span><span class="p">[:,</span> <span class="mi">0</span><span class="p">]</span><span class="o">.</span><span class="n">max</span><span class="p">()</span> <span class="o">+</span> <span class="mf">0.1</span>
<span class="n">y_min</span><span class="p">,</span> <span class="n">y_max</span> <span class="o">=</span> <span class="n">reduced_data</span><span class="p">[:,</span> <span class="mi">1</span><span class="p">]</span><span class="o">.</span><span class="n">min</span><span class="p">()</span> <span class="o">-</span> <span class="mf">0.1</span><span class="p">,</span> <span class="n">reduced_data</span><span class="p">[:,</span> <span class="mi">1</span><span class="p">]</span><span class="o">.</span><span class="n">max</span><span class="p">()</span> <span class="o">+</span> <span class="mf">0.1</span>
<span class="n">X</span><span class="p">,</span> <span class="n">Y</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">meshgrid</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">arange</span><span class="p">(</span><span class="n">x_min</span><span class="p">,</span> <span class="n">x_max</span><span class="p">,</span> <span class="n">h</span><span class="p">),</span> <span class="n">np</span><span class="o">.</span><span class="n">arange</span><span class="p">(</span><span class="n">y_min</span><span class="p">,</span> <span class="n">y_max</span><span class="p">,</span> <span class="n">h</span><span class="p">))</span>

<span class="c"># Obtain labels for each point in mesh. Use last trained model.</span>
<span class="n">me</span> <span class="o">=</span> <span class="n">kmeans</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">reduced_data</span><span class="p">[</span><span class="mi">0</span><span class="p">])</span>
<span class="k">print</span> <span class="n">reduced_data</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span>
<span class="k">print</span> <span class="n">me</span>

<span class="n">Z</span> <span class="o">=</span> <span class="n">kmeans</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">c_</span><span class="p">[</span><span class="n">X</span><span class="o">.</span><span class="n">ravel</span><span class="p">(),</span> <span class="n">Y</span><span class="o">.</span><span class="n">ravel</span><span class="p">()])</span>

<span class="c"># Put the result into a color plot</span>
<span class="n">Z</span> <span class="o">=</span> <span class="n">Z</span><span class="o">.</span><span class="n">reshape</span><span class="p">(</span><span class="n">X</span><span class="o">.</span><span class="n">shape</span><span class="p">)</span>
</pre></div>


    [-0.07764109  0.04700812]
    [3]


### Plot the data

<div class="highlight"><pre><span class="n">figure</span><span class="p">(</span><span class="n">figsize</span><span class="o">=</span><span class="p">(</span><span class="mi">12</span><span class="p">,</span> <span class="mi">12</span><span class="p">))</span>
<span class="n">clf</span><span class="p">()</span>
<span class="n">imshow</span><span class="p">(</span><span class="n">Z</span><span class="p">,</span> <span class="n">interpolation</span><span class="o">=</span><span class="s">&#39;nearest&#39;</span><span class="p">,</span>
          <span class="n">extent</span><span class="o">=</span><span class="p">(</span><span class="n">X</span><span class="o">.</span><span class="n">min</span><span class="p">(),</span> <span class="n">X</span><span class="o">.</span><span class="n">max</span><span class="p">(),</span> <span class="n">Y</span><span class="o">.</span><span class="n">min</span><span class="p">(),</span> <span class="n">Y</span><span class="o">.</span><span class="n">max</span><span class="p">()),</span>
          <span class="n">cmap</span><span class="o">=</span><span class="n">cm</span><span class="o">.</span><span class="n">Paired</span><span class="p">,</span>
          <span class="n">aspect</span><span class="o">=</span><span class="s">&#39;auto&#39;</span><span class="p">,</span> <span class="n">origin</span><span class="o">=</span><span class="s">&#39;lower&#39;</span><span class="p">)</span>

<span class="n">plot</span><span class="p">(</span><span class="n">reduced_data</span><span class="p">[:,</span> <span class="mi">0</span><span class="p">],</span> <span class="n">reduced_data</span><span class="p">[:,</span> <span class="mi">1</span><span class="p">],</span> <span class="s">&#39;k.&#39;</span><span class="p">,</span> <span class="n">markersize</span><span class="o">=</span><span class="mi">2</span><span class="p">)</span>
<span class="c"># Plot the centroids as a white X</span>
<span class="n">centroids</span> <span class="o">=</span> <span class="n">kmeans</span><span class="o">.</span><span class="n">cluster_centers_</span>
<span class="n">scatter</span><span class="p">(</span><span class="n">centroids</span><span class="p">[:,</span> <span class="mi">0</span><span class="p">],</span> <span class="n">centroids</span><span class="p">[:,</span> <span class="mi">1</span><span class="p">],</span>
           <span class="n">marker</span><span class="o">=</span><span class="s">&#39;x&#39;</span><span class="p">,</span> <span class="n">s</span><span class="o">=</span><span class="mi">169</span><span class="p">,</span> <span class="n">linewidths</span><span class="o">=</span><span class="mi">3</span><span class="p">,</span>
           <span class="n">color</span><span class="o">=</span><span class="s">&#39;w&#39;</span><span class="p">,</span> <span class="n">zorder</span><span class="o">=</span><span class="mi">10</span><span class="p">)</span>

<span class="n">plot</span><span class="p">(</span><span class="n">reduced_data</span><span class="p">[</span><span class="n">labels</span> <span class="o">==</span> <span class="mi">0</span><span class="p">,</span> <span class="mi">0</span><span class="p">],</span>
        <span class="n">reduced_data</span><span class="p">[</span><span class="n">labels</span> <span class="o">==</span> <span class="mi">0</span><span class="p">,</span> <span class="mi">1</span><span class="p">],</span> <span class="s">&#39;r.&#39;</span><span class="p">,</span> <span class="n">markersize</span><span class="o">=</span><span class="mi">20</span><span class="p">)</span>
<span class="n">text</span><span class="p">(</span><span class="n">reduced_data</span><span class="p">[</span><span class="mi">0</span><span class="p">,</span> <span class="mi">0</span><span class="p">],</span> <span class="n">reduced_data</span><span class="p">[</span><span class="mi">0</span><span class="p">,</span> <span class="mi">1</span><span class="p">],</span> <span class="s">&#39;David Leen&#39;</span><span class="p">)</span>

<span class="n">plot</span><span class="p">(</span><span class="n">reduced_data</span><span class="p">[</span><span class="n">labels</span> <span class="o">==</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">0</span><span class="p">],</span>
        <span class="n">reduced_data</span><span class="p">[</span><span class="n">labels</span> <span class="o">==</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">1</span><span class="p">],</span> <span class="s">&#39;b.&#39;</span><span class="p">,</span> <span class="n">markersize</span><span class="o">=</span><span class="mi">10</span><span class="p">)</span>
<span class="n">plot</span><span class="p">(</span><span class="n">reduced_data</span><span class="p">[</span><span class="n">labels</span> <span class="o">==</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">0</span><span class="p">],</span>
        <span class="n">reduced_data</span><span class="p">[</span><span class="n">labels</span> <span class="o">==</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">1</span><span class="p">],</span> <span class="s">&#39;g.&#39;</span><span class="p">,</span> <span class="n">markersize</span><span class="o">=</span><span class="mi">10</span><span class="p">)</span>
<span class="n">plot</span><span class="p">(</span><span class="n">reduced_data</span><span class="p">[</span><span class="n">labels</span> <span class="o">==</span> <span class="mi">3</span><span class="p">,</span> <span class="mi">0</span><span class="p">],</span>
        <span class="n">reduced_data</span><span class="p">[</span><span class="n">labels</span> <span class="o">==</span> <span class="mi">3</span><span class="p">,</span> <span class="mi">1</span><span class="p">],</span> <span class="s">&#39;c.&#39;</span><span class="p">,</span> <span class="n">markersize</span><span class="o">=</span><span class="mi">10</span><span class="p">)</span>

<span class="k">for</span> <span class="n">i</span><span class="p">,</span> <span class="n">n</span> <span class="ow">in</span> <span class="nb">enumerate</span><span class="p">(</span><span class="n">sm</span><span class="o">.</span><span class="n">simply_measured_people</span><span class="p">,</span> <span class="n">start</span><span class="o">=</span><span class="mi">1</span><span class="p">):</span>
    <span class="n">text</span><span class="p">(</span><span class="n">reduced_data</span><span class="p">[</span><span class="n">i</span><span class="p">,</span> <span class="mi">0</span><span class="p">],</span> <span class="n">reduced_data</span><span class="p">[</span><span class="n">i</span><span class="p">,</span> <span class="mi">1</span><span class="p">],</span> <span class="n">n</span><span class="p">)</span>

<span class="n">title</span><span class="p">(</span><span class="s">&#39;K-means clustering on the digits dataset (PCA-reduced data)</span><span class="se">\n</span><span class="s">&#39;</span>
      <span class="s">&#39;Centroids are marked with white cross&#39;</span><span class="p">)</span>
<span class="n">xlim</span><span class="p">(</span><span class="n">x_min</span><span class="p">,</span> <span class="n">x_max</span><span class="p">),</span> <span class="n">ylim</span><span class="p">(</span><span class="n">y_min</span><span class="p">,</span> <span class="n">y_max</span><span class="p">)</span>
<span class="n">xticks</span><span class="p">(()),</span> <span class="n">yticks</span><span class="p">(())</span>
<span class="n">show</span><span class="p">()</span>
</pre></div>



![](company_culture_fit_files/company_culture_fit_fig_00.png)


<div class="highlight"><pre><span class="kn">from</span> <span class="nn">sklearn.mixture</span> <span class="kn">import</span> <span class="n">GMM</span>


<span class="k">def</span> <span class="nf">make_ellipses</span><span class="p">(</span><span class="n">gmm</span><span class="p">,</span> <span class="n">ax</span><span class="p">):</span>
    <span class="k">for</span> <span class="n">n</span><span class="p">,</span> <span class="n">color</span> <span class="ow">in</span> <span class="nb">enumerate</span><span class="p">(</span><span class="s">&#39;rgb&#39;</span><span class="p">):</span>
        <span class="n">v</span><span class="p">,</span> <span class="n">w</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">linalg</span><span class="o">.</span><span class="n">eigh</span><span class="p">(</span><span class="n">gmm</span><span class="o">.</span><span class="n">_get_covars</span><span class="p">()[</span><span class="n">n</span><span class="p">][:</span><span class="mi">2</span><span class="p">,</span> <span class="p">:</span><span class="mi">2</span><span class="p">])</span>
        <span class="n">u</span> <span class="o">=</span> <span class="n">w</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">/</span> <span class="n">np</span><span class="o">.</span><span class="n">linalg</span><span class="o">.</span><span class="n">norm</span><span class="p">(</span><span class="n">w</span><span class="p">[</span><span class="mi">0</span><span class="p">])</span>
        <span class="n">angle</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">arctan2</span><span class="p">(</span><span class="n">u</span><span class="p">[</span><span class="mi">1</span><span class="p">],</span> <span class="n">u</span><span class="p">[</span><span class="mi">0</span><span class="p">])</span>
        <span class="n">angle</span> <span class="o">=</span> <span class="mi">180</span> <span class="o">*</span> <span class="n">angle</span> <span class="o">/</span> <span class="n">np</span><span class="o">.</span><span class="n">pi</span>  <span class="c"># convert to degrees</span>
        <span class="n">v</span> <span class="o">*=</span> <span class="mi">9</span>
        <span class="n">ell</span> <span class="o">=</span> <span class="n">mpl</span><span class="o">.</span><span class="n">patches</span><span class="o">.</span><span class="n">Ellipse</span><span class="p">(</span><span class="n">gmm</span><span class="o">.</span><span class="n">means_</span><span class="p">[</span><span class="n">n</span><span class="p">,</span> <span class="p">:</span><span class="mi">2</span><span class="p">],</span> <span class="n">v</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span> <span class="n">v</span><span class="p">[</span><span class="mi">1</span><span class="p">],</span>
                                  <span class="mi">180</span> <span class="o">+</span> <span class="n">angle</span><span class="p">,</span> <span class="n">color</span><span class="o">=</span><span class="n">color</span><span class="p">)</span>
        <span class="n">ell</span><span class="o">.</span><span class="n">set_clip_box</span><span class="p">(</span><span class="n">ax</span><span class="o">.</span><span class="n">bbox</span><span class="p">)</span>
        <span class="n">ell</span><span class="o">.</span><span class="n">set_alpha</span><span class="p">(</span><span class="mf">0.5</span><span class="p">)</span>
        <span class="n">ax</span><span class="o">.</span><span class="n">add_artist</span><span class="p">(</span><span class="n">ell</span><span class="p">)</span>
</pre></div>



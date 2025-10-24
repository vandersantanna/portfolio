<small align="right">Contact: <a href="mailto:vandersantanna@gmail.com">Email</a> · <a href="https://www.linkedin.com/in/vandersantanna">LinkedIn</a> · <a href="https://github.com/vandersantanna">GitHub</a></small>

# ⚡ SQL Tuning & Query Optimization  

## 📌 Overview  
This section highlights my expertise in **SQL performance tuning** and **query optimization**.  
With over **30 years of experience** across **Oracle, SQL Server, PostgreSQL, and MySQL**,  
I have worked extensively on analyzing execution plans, rewriting queries, and designing indexing strategies  
to optimize mission-critical systems with millions of transactions.  

---

## 🎯 Areas of Expertise  
- Query plan analysis and optimization  
- Indexing strategies (B-tree, bitmap, covering indexes, composite keys)  
- Partitioning and table design for performance  
- SQL rewrite and refactoring for efficiency  
- Identifying and eliminating performance bottlenecks  
- Optimizing joins, subqueries, and nested views  
- Reducing locking, blocking, and deadlocks  
- Monitoring and tuning high-throughput systems  

---

## 🔧 Example 1 — Oracle SQL Tuning  
**Scenario:** A financial system with slow reporting queries.  
**Problem:** Full table scans on a table with 50M+ rows.  
**Solution:**  
- Added a composite index on `(customer_id, transaction_date)`  
- Rewrote nested queries into joins with proper filtering  
- Implemented table partitioning by transaction_date  
**Result:** Reduced query execution time from **45 minutes → 30 seconds**.  

---

## 🔧 Example 2 — SQL Server Query Optimization  
**Scenario:** Deadlocks occurring in a high-concurrency OLTP environment.  
**Problem:** Poor indexing and inconsistent isolation levels.  
**Solution:**  
- Created covering indexes for frequently accessed columns  
- Refactored queries to avoid unnecessary locking hints  
- Applied row-versioning isolation (RCSI) to reduce contention  
**Result:** Deadlocks dropped by **90%**, throughput increased by **40%**.  

---

## 🔧 Example 3 — PostgreSQL Query Rewrite  
**Scenario:** Analytics queries in PostgreSQL taking hours.  
**Problem:** Badly written subqueries and missing statistics.  
**Solution:**  
- Enabled extended statistics on correlated columns  
- Rewrote subqueries into CTEs with materialization disabled  
- Implemented partial indexes for selective filters  
**Result:** Execution reduced from **2h → 5 minutes**.  

---
[Back to top](#table-of-contents)

---

**[🏠 Back to Main Portfolio](../README.md#top)**

---

## Author & Maintainer
<table>
  <tr>
    <td width="96" valign="top">
      <img src="https://github.com/vandersantanna.png?size=160" alt="Vanderley Sant Anna" width="96" height="96">
    </td>
    <td valign="top">
      <strong>Vanderley Sant Anna</strong><br>
      Senior Database Engineer (DBE) / Senior Database Reliability Engineer (DBRE) / Senior DBA / DataOps Engineer
    </td>
  </tr>
</table>

**Preferred name:** Vander  

**Education:**  
- B.Sc. in Software Engineering — Centro Universitário de Maringá (UniCesumar) — *UniCesumar University Center*, Maringá, Brazil (2020)  
- Postgraduate Specialization (Lato Sensu) in Software Project Engineering — Universidade do Sul de Santa Catarina (UNISUL) — *Southern Santa Catarina University*, Florianópolis, Brazil (2008)  
- Technologist in Data Processing (*Tecnólogo em Processamento de Dados*) — Universidade do Estado de Santa Catarina (UDESC) — *Santa Catarina State University*, Joinville, Brazil (1995)  

**Certifications:**  
- Oracle OCP  
- MongoDB University — M102: MongoDB for DBAs  
- IBM Certified Database Associate — DB2 9 Fundamentals  

**Location & Timezone:** Blumenau, SC, Brazil (UTC−3) • **Availability:** Remote (Americas & Europe)

**Last Updated:** 2025-10-24 • **Status:** Actively maintained

## 📫 Contact
- **Email (primary):** [vandersantanna@gmail.com](mailto:vandersantanna@gmail.com)  
- **LinkedIn:** [linkedin.com/in/vandersantanna](https://www.linkedin.com/in/vandersantanna)  
- **GitHub:** [github.com/vandersantanna](https://github.com/vandersantanna)

<details>
  <summary><strong>Trademarks</strong></summary>

  <small>All product names, logos, and brands are property of their respective owners. 
  Use of these names is for identification purposes only and does not imply endorsement or affiliation.</small>
</details>

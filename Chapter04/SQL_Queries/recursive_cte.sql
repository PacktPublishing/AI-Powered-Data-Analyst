-- RECURSIVE CTE to traverse organizational hierarchy from top (CEO) down to all employees 

WITH RECURSIVE org_tree AS ( 
   -- ANCHOR MEMBER: Select all top-level employees (those with no manager) 
   SELECT  
       employee_id, 
       name, 
       manager_id, 
       CAST(NULL AS VARCHAR(100)) AS manager_name,  -- Top-level has no manager 
       1 AS hierarchy_level, 
       CAST(name AS VARCHAR(500)) AS full_path,      -- Path starts with their own name 
       1 AS depth_tracker  -- Used to enforce depth_limit of 10 
   FROM employees 
   WHERE manager_id IS NULL 
    
   UNION ALL 
    
   -- RECURSIVE MEMBER: Join employees to their managers from the anchor 
   -- This finds all direct reports of employees already in the CTE 
   -- Each iteration goes one level deeper in the hierarchy 
   SELECT  
       e.employee_id, 
       e.name, 
       e.manager_id, 
       ot.name AS manager_name,  -- Get manager name from the CTE (previous level) 
       ot.hierarchy_level + 1 AS hierarchy_level,  -- Increment level by 1 
       -- Build the full path by concatenating parent path with ' > ' and current employee name 
       -- Example: 'CEO > VP Sales' becomes 'CEO > VP Sales > Regional Manager' 
       CAST(ot.full_path || ' > ' || e.name AS VARCHAR(500)) AS full_path, 
       ot.depth_tracker + 1 AS depth_tracker  -- Increment depth counter 
   FROM employees e 
   INNER JOIN org_tree ot ON e.manager_id = ot.employee_id  -- Connect employee to their manager 
   WHERE ot.depth_tracker < 10  -- DEPTH LIMIT: Prevents infinite loops and limits to 10 levels 
 
-- Final SELECT: Output the complete hierarchy with all reporting information 
-- Ordered by hierarchy_level (top to bottom) and then by name alphabetically 
SELECT  
   employee_id, 
   name, 
   COALESCE(manager_name, 'Top Level (CEO/C-Suite)') AS manager_name,  -- Pretty display for top level 
   hierarchy_level, 
   full_path, 
   depth_tracker AS actual_depth 
FROM org_tree 
ORDER BY hierarchy_level, name; 

Rationale
=========

Why another drag-and-drop ordering plugin?
------------------------------------------

Other projects have added drag-and-drop ordering to the ChangeList view, however this introduces a couple of problems...

- The ChangeList view supports pagination, which makes drag-and-drop ordering across pages impossible.
- The ChangeList view by default, does not order records based on a foreign key, nor distinguish between rows that are associated with a foreign key. This makes ordering the records grouped by a foreign key impossible.
- The ChangeList supports in-line editing, and adding drag-and-drop ordering on top of that just seemed a little much in my opinion.

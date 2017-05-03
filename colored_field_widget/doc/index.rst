Colored field widget
====================

Module provide widgets to color some fields in list view

.. toctree::

Colored Widget
--------------

Widget allow you to mark field with color based on condition.

To use this widget, you must set some attributes in field definition. Can be used for all fields, that displays
as text.

.. code-block:: xml

    <field name="name" widget="colored" check="mark_color" hover_title="type_id"/>

:check: if this field has value and it's value not False, original field will be colored.
:hover_title: (optional) define field, witch text will be used for tooltip instead of field help text.
:color: (optional) define color, that will be used to colored field. Default is `red`.
:other_style: (optional) define other text, that will be used in style attribute. Default is ``.

Colored Boolean Widget
----------------------

Widget allow you to add to selection field colored text based on condition.

To use this widget, you must set some attributes in field definition. Can be used for boolean fields.

.. code-block:: xml

    <field name="is_currency" widget="bool_colored" check="old_is_currency" hover_title="old_is_currency"  color="blue" check_text="Changed"/>

:check: if this field has value and it's value not False, original field will be colored.
:check_text: text, that will be displayed, when condition is true
:hover_title: (optional) define field, witch text will be used for tooltip instead of field help text.
:color: (optional) define color, that will be used to colored field. Default is `red`.
:other_style: (optional) define other text, that will be used in style attribute. Default is ``.
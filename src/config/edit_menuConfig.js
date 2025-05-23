export const edit_menuConfig = {
    name: "edit_menu",
    tiles : [
        {
          type: "textarea",
          colspan: 2
        },
        {
          type: "switch",
          label: "Back",
          action: { type: "switch_view", view: "writing" }
        },
        {
          type: "switch",
          label: "Navigation",
          action: { type: "switch_view", view: "navigation_menu" }
        },
        {
          type : "editing",
          label : "Delete Section",
          action : {type : "delete_section"}
        },
        {
          type : "editing",
          label : "Delete Sentence",
          action : {type : "delete_sentence"}

        },
        {
          type : "editing",
          label : "Delete Word",
          action : { type: "delete_word"}
        },
        { 
          type: "delete",
          label: "DELETE",
          action: { type: "delete_letter_edit" }
        }
      ]
  };
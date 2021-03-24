#!/bin/bash

#gets only the lines within the <td> tag and pipe to the next command
grep '<td>.*</td>' |

#remove all the html tags and pipe it to the next command
sed 's/<[^>]*>//g' |

#delete all the empty lines ([^$] literally matches to empty lines) and pipe it to the next command
sed '/^$/d' |

#output only the odd number lines which are the Hawaiian words and pipe to the next command
sed -n '0~2p' |

#lowercase everything and pipe to the next command
tr [A-Z] [a-z] |

#replace all instances of ` with '
sed "s/\`/\'/g" |

#replace all instances of commas with newlines
sed 's/\,/\n/g' | 

#replace all instances of spaces with newlines
sed 's/ /\n/g' |

#delete any empty lines that were made from the previous chain of commands
sed 's/^$/d' |

#remove all words that don't contain Hawaiian characters
sed "/[^pk'mnwlhaeiou]/d" |

#sort them and remove the duplicates
sort -u

